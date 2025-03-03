#!/usr/bin/env python3
#
# Copyright (c)  2025  DeepModal Inc.
# Written by Hoon Chung (hchung@etri.re.kr)

import argparse
import asyncio
import logging
import wave
from typing import List, Tuple
import numpy as np
import time
import os
import struct
try:
  import websockets
  import librosa
except ImportError:
  print("")
  print("  pip install websockets librosa" )
  print("")
import websockets
import librosa

def get_args():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )

  parser.add_argument(
    "--server-addr",
    type=str,
    default="15.164.166.78",
    help="Address of the server (default AWS server)",
  )

  parser.add_argument(
    "--server-port",
    type=int,
    default=7000,
    help="Port of the server",
  )
  
  parser.add_argument(
    "--client-code",
    type=int,
    default=8000,
    help="Code of the server API",
  )

  parser.add_argument(
    "audio_files",
    type=str,
    nargs="+",
    help="The input audio files (supports various formats like WAV, MP3, FLAC, etc.)",
  )
  return parser.parse_args()

def read_audio(audio_filename: str) -> Tuple[np.ndarray, int]:
  """Read any audio format and resample to 8kHz mono."""
  target_sr = 8000
  
  try:
    # Load audio file with librosa (supports various formats)
    y, sr = librosa.load(audio_filename, sr=None, mono=True)
    
    # Resample to 8kHz if needed
    if sr != target_sr:
      logging.info(f"Resampling from {sr}Hz to {target_sr}Hz")
      y = librosa.resample(y, orig_sr=sr, target_sr=target_sr)
    
    # Ensure float32 type
    y = y.astype(np.float32)
    
    # Clip to 30 seconds if longer
    max_samples = target_sr * 30
    if len(y) > max_samples:
      logging.warning(f"Demo supports up to 30 seconds, truncating to 30 seconds")
      y = y[:max_samples]
    
    return y, target_sr
    
  except Exception as e:
    logging.error(f"Error reading audio file {audio_filename}: {e}")
    raise

def encode_audio_data(client_code: int, samples: np.ndarray) -> bytes:
  """Encodes client code and audio sample data into a byte stream."""
  return (
    struct.pack("<II", client_code, samples.size * 4) + samples.tobytes()
  )

async def process_audio(websocket, audio_filename: str, client_code: int):
  """Processes a single audio file and sends it to the server."""
  logging.info(f"Processing {audio_filename}")

  # Read and resample audio
  samples, sample_rate = read_audio(audio_filename)
  wav_duration = len(samples) / sample_rate
  assert isinstance(sample_rate, int)
  assert samples.dtype == np.float32, samples.dtype
  assert samples.ndim == 1, samples.ndim

  # Send audio data
  start_time = time.time()
  buf = encode_audio_data(client_code, samples)
  if buf:
    await websocket.send(buf)

  # Receive results
  results = await websocket.recv()
  elapsed_time = time.time() - start_time
  rtf = elapsed_time / wav_duration
  print(f"{results}, RTF={rtf:.2f} on AWS EC2 t2.micro [1 vCPU, 1 GB]")

async def run(server_addr: str, server_port: int, client_code: int, audio_files: List[str]):
  """Runs the WebSocket client to send audio files to the server."""
  uri = f"ws://{server_addr}:{server_port}"
  async with websockets.connect(uri) as websocket:
    for audio_filename in audio_files:
      await process_audio(websocket, audio_filename, client_code)
        
    # Send termination signal
    await websocket.send("Done")

async def main():
  args = get_args()
  logging.info(vars(args))

  server_addr = args.server_addr
  server_port = args.server_port
  client_code = args.client_code
  audio_files = args.audio_files

  await run(
    server_addr=server_addr,
    server_port=server_port,
    client_code=client_code,
    audio_files=audio_files,
  )

if __name__ == "__main__":
  formatter = (
    "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"  # noqa
  )
  logging.basicConfig(format=formatter, level=logging.INFO)
  asyncio.run(main())
