# PhonicFlow-Lite

*PhoneFlow-Lite*는 (주)딥모달의 음성인식 기술로
- 국내 최고 수준의 음성 인식 정확도와 
- AWS EC2 t2.micro 서버(1 vCPU, 1GB)에서 평균 0.25xRT의 고속 디코딩을 지원합니다

## 1. 설치
파이썬 평가 프로그램을 사용하기 위해서는 websockets와 librosa 패키지를 설치해야 합니다
```
git clone https://github.com/deep-modal/phonicflow.git
cd phonicflow
pip install websockets librosa
```

## 2. 평가
음성 인식 결과 및 RTF는 다음의 명령어를 사용해 확인 할 수 있습니다.
```
python examples/phonicflow-websocket-client.py audio/phonecall-clip-1.wav audio/phonecall-clip-2.wav audio/youtube-clip-1.mp3
```

AICC용 모델은 다음 포트로 평가해 볼수 있습니다.
```
python examples/phonicflow-websocket-client.py --server-port "81/aicc/" audio/phonecall-clip-1.wav audio/phonecall-clip-2.wav
```

## 3. 문의
Phrase Hint, API 기능 및 협업 관련한 사항은 딥모달(hchung@etri.re.kr)로 연락 주십시요.
