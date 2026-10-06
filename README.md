# Python OpenAI Logs 실습 프로젝트

Python 가상환경에서 Responses API를 호출하고, OpenAI Platform Logs에서 요청과 답변을 확인하는 초보자용 예제입니다. Python 3.10 이상을 사용하세요.

## 포함된 파일

```text
openai-logs-demo/
├── main.py           # API 호출 및 설정 확인
├── requirements.txt  # 필요한 라이브러리
├── .env.example      # 환경 설정 샘플
├── .gitignore        # 키 및 가상환경을 Git에서 제외
└── README.md         # 설치 및 실행 안내
```

`.env`와 `.venv`는 아래 과정을 따라 로컬에서 생성합니다. 실제 키는 제공된 파일에 포함되어 있지 않습니다.

## 1. Windows PowerShell에서 프로젝트 폴더 열기

압축 파일을 풀고 `main.py`가 있는 폴더에서 PowerShell 또는 VS Code 터미널을 엽니다.

```powershell
python --version
python -m venv .venv
```

`python` 대신 `py`만 동작한다면 위 두 명령의 `python`을 `py`로 바꾸세요. 둘 다 동작하지 않으면 Python 3.10 이상을 먼저 설치하고 터미널을 다시 여세요.

## 2. 가상환경 활성화 및 설치

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

앞에 `(.venv)`가 나타나면 활성화된 것입니다. 가상환경에는 이 프로젝트의 라이브러리가 별도로 설치됩니다.

PowerShell에서 스크립트 실행이 차단되면 활성화 없이 아래처럼 가상환경의 Python을 직접 사용할 수 있습니다. 시스템 정책을 변경할 필요가 없습니다.

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

이 방식을 선택했다면 아래 실행 명령의 `python`도 `.\.venv\Scripts\python.exe`로 바꾸세요.

## 3. .env 만들기

```powershell
Copy-Item .env.example .env
notepad .env
```

이미 `.env`를 만들었다면 복사 명령을 다시 실행하지 말고 기존 파일을 편집하세요. 아래 값에서 `your_api_key_here`만 실제 API 키로 변경하고 저장합니다.

```dotenv
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

키는 [OpenAI Platform API Keys](https://platform.openai.com/api-keys)에서 확인하거나 생성하세요. 키를 채팅이나 GitHub에 올리지 마세요. API 사용에는 별도의 API 결제 설정이 필요하며 사용 요금이 발생할 수 있습니다.

`main.py`는 `python-dotenv`로 자신의 폴더에 있는 `.env`를 읽습니다. 이 실습은 `override=True`를 사용하여 `.env`의 값이 기존 환경 변수보다 우선하도록 구성했습니다. `.env`는 일반 텍스트 파일이며 `.gitignore`는 암호화가 아닌 Git 업로드 제외 설정입니다.

## 4. 설정만 확인하기 — API 호출 없음

```powershell
python main.py --check
```

키 값은 출력하지 않습니다. 이 명령은 설정 여부만 확인하며 키의 실제 유효성, 크레딧 또는 모델 권한은 확인하지 않습니다.

## 5. 실제 API 호출하기

```powershell
python main.py
```

다른 질문을 보내려면:

```powershell
python main.py --prompt "가상환경이 무엇인지 초보자에게 설명해줘."
```

답변, `resp_...` 형태의 응답 ID, 응답 상태, Logs 주소가 표시됩니다. 재실행할 때마다 새로운 API 요청을 보냅니다. 이 예제는 자동 재시도를 꺼두었으며 요청 제한 시간은 60초입니다.

## 6. Platform Logs 확인하기

1. [Responses Logs](https://platform.openai.com/logs?api=responses)를 엽니다.
2. API 키를 만든 조직과 프로젝트를 선택합니다.
3. 날짜 범위와 검색 조건을 확인하고 새로고침합니다.
4. 방금 보낸 요청을 열어 입력과 출력을 확인합니다.

`client.responses.create(..., store=True)`가 응답을 저장하도록 요청합니다. `print()`는 터미널 표시용입니다. 공식 문서는 Response 객체의 기본 저장 기간을 30일로 안내합니다. 조직이나 프로젝트에 Zero Data Retention이 적용되어 있으면 `store=True`도 `false`로 처리됩니다.

## macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
# 편집기로 .env를 열고 API 키 입력
python main.py --check
python main.py
```

## 자주 만나는 문제

| 문제 | 해결 방법 |
|---|---|
| `No module named openai` 또는 `dotenv` | 가상환경의 Python으로 requirements.txt 설치 |
| API 키 설정 오류 | `.env.txt`가 아닌 `.env`인지, 실제 키를 입력했는지 확인 |
| 인증 오류 | 만료되거나 삭제된 키인지 확인 |
| 한도 오류 | API 크레딧, 사용 한도 또는 요청 속도 확인 |
| 모델 관련 오류 | `.env`의 모델 이름과 프로젝트 사용 권한 확인 |
| 연결 오류 | 인터넷 연결 확인. 결과가 불명확하면 재실행 전 Logs 확인 |
| Logs가 비어 있음 | 조직, 프로젝트, 날짜 필터와 데이터 보존 설정 확인 |

가상환경을 종료하려면 활성화한 터미널에서 `deactivate`를 실행합니다.

## 참고 문서

- [OpenAI Python SDK 및 .env 안내](https://developers.openai.com/api/reference/python)
- [Responses 저장과 Logs](https://developers.openai.com/api/docs/guides/conversation-state)
- [데이터 보존 설정](https://developers.openai.com/api/docs/guides/your-data)
- [python-dotenv 문서](https://bbc2.github.io/python-dotenv/)
