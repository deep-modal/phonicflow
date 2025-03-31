# PhonicFlow-Lite Technical Report

## 1. PhonicFlow-Lite

PhonicFlow-Lite는 (주)딥모달의 음성인식 기술로 높은 정확도와 쓰루풋을 제공하며, 일반 음성 인식 모델과 AICC 전용 모델을 서비스하고 있습니다.

### 모델 URL

- **General**: `ws://deepmodal.ai:81/ws/`
- **AICC**: `ws://deepmodal.ai:81/aicc/`

## 2. PhonicFlow-Lite 성능

### 음성인식 정확도
음성 인식 정확도는 **CER(Character Error Rate)** 로 측정하였습니다.

\[CER = (S + I + D) / N\]

- **S**: 치환 오류 갯수
- **I**: 삽입 오류 갯수
- **D**: 삭제 오류 갯수
- **N**: 전체 문자 갯수

| 데이터셋 | CER(%) |
|----------|-------|
| 비대면 진료를 위한 의료진 및 환자 음성 | 0.96 |
| 고객 응대 음성 | 1.95 |
| 상담 음성 | 2.60 |

### 디코딩 속도
디코딩 속도는 단일 쓰레드에서의 **RTF(Real-time Factor)** 로 측정하였습니다.

\[xRT = processing time / audio length\]

| CPU | xRT |
|------|------|
| AWS t2.micro | 0.25 |
| Intel(R) Xeon(R) Gold 6426Y | 0.05 |

## 3. 디코딩 속도

### 3.1 On-premise 평가 환경

- **CPU**: Intel(R) Xeon(R) Gold 6426Y (2.5GHz, 2-CPU, 16-core/CPU)
- **오디오파일-1**: `2.Validation/원천데이터/공중파방송/버라이어티쇼 예능/SLAAJ21000064.wav` (3326.951초)
- **오디오파일-2**: `2.Validation/원천데이터/공중파방송/정치 경제/SLAAT21000007.wav` (3650초)

### 3.2 On-premise 평가 결과

| Threads | Elapsed-time (s) | xRT |
|---------|----------------|----|
| 1 | 153 | 0.046 |
| 2 | 98 | 0.029 |
| 4 | 68 | 0.021 |
| 8 | 58 | 0.017 |
| 16 | 57 | 0.017 |

### 3.3 서버-클라이언트 동시 접속 평가 환경

- **Client**: LG-Gram 노트북, 공공 WIFI 망
- **Server**: Intel(R) Xeon(R) Gold 6426Y (2.5GHz, 2-CPU, 16-core/CPU)
- **오디오파일**: `2.Validation/원천데이터/공중파방송/정치 경제/SLAAT21000007.wav` (3650초)

### 3.4 서버-클라이언트 동시 접속 평가 결과

| Client 수 | 서버 Thread 수 | Elapsed-time (s) | xRT |
|-----------|--------------|----------------|----|
| 1 | 1 | 227 | 0.06 |
| 4 | 1 | 831 | 0.23 |
| 8 | 1 | 1542 | 0.43 |
| 1 | 2 | 155 | 0.04 |
| 4 | 2 | 210 | 0.11 |
| 8 | 2 | 1003 | 0.30 |

## 4. 평가용 코드

다음 PhonicFlow 저장소의 코드를 사용하여 평가를 할 수 있습니다.

### 1. 평가 환경 설정
```sh
git clone https://github.com/deep-modal/phonicflow.git
cd phonicflow
pip install websockets librosa
```

### 2. 일반 모델 평가
```sh
python examples/phonicflow-websocket-client.py audio/phonecall-clip-1.wav
```

### 3. AICC 모델 평가
```sh
python examples/phonicflow-websocket-client.py -server-port "81/aicc/" audio/phonecall-clip-1.wav
```

## 5. 문의

기술 도입, 협업 및 기타 문의 사항은 (주)딥모달 `hchung@etri.re.kr`로 연락 주십시오.

