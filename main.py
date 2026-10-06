# 프로젝트 이름: OpenAI Responses Logs 실습
# 설명: 커맨드라인 질문을 Responses API로 보내고 답변과 Logs 확인 정보를 출력함
# 작성자: 서진호
# 버전: V1.0.0
# 실행 예시: python main.py --prompt "안녕하세요"
# 설정 확인: python main.py --check

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, AuthenticationError, OpenAI, RateLimitError

# 실행 폴더가 달라도 설정 파일을 찾도록 현재 소스 파일의 폴더를 기준으로 함
PROJECT_DIR = Path(__file__).resolve().parent

# 요청 내역을 확인할 OpenAI 플랫폼의 Responses Logs 주소
LOGS_URL = "https://platform.openai.com/logs?api=responses"


def main() -> int:
    # 설정 확인, API 요청, 결과 출력을 담당하는 진입 함수
    # 정상 종료 시 0, 입력·설정 또는 API 오류 발생 시 1을 반환함

    # 커맨드라인에서 질문과 설정 확인 여부를 받고, 질문이 없으면 기본 문장을 사용함
    parser = argparse.ArgumentParser(description="OpenAI Responses Logs 실습")
    parser.add_argument("--prompt", default="파이썬을 처음 배우는 사람에게 응원 한 문장을 한국어로 써줘.")
    parser.add_argument("--check", action="store_true", help="API 요청 없이 설정만 확인")
    args = parser.parse_args()

    # 실행 위치와 관계없이 main.py 옆의 .env를 읽음
    # 이 실습에서는 .env 값이 기존 환경 변수보다 우선함
    load_dotenv(PROJECT_DIR / ".env", override=True, encoding="utf-8-sig")

    # 키와 모델 이름의 앞뒤 공백을 제거하고 모델 설정이 없으면 기본값을 사용함
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()

    # 실제 요청 전에 비어 있는 값과 예제용 API 키를 검사함
    if not api_key or api_key == "your_api_key_here":
        print("설정 오류: .env의 OPENAI_API_KEY에 실제 API 키를 입력하세요.")
        return 1
    if not model:
        print("설정 오류: .env의 OPENAI_MODEL을 입력하세요.")
        return 1
    if not args.prompt.strip():
        print("입력 오류: 질문을 입력하세요.")
        return 1
    # --check는 설정 값만 검사하며 API 요청이나 키 인증을 수행하지 않습니다.
    if args.check:
        print(f"설정 확인 완료 / 모델: {model}")
        print("API 키 값은 표시하지 않습니다. 유효성 및 API 접속은 확인하지 않았습니다.")
        return 0

    try:
        # 클라이언트는 블록 종료 시 정리하며, 제한 시간은 60초로 설정함
        # 자동 재시도는 끄고 오류가 나면 사용자가 결과를 확인하도록 함
        with OpenAI(api_key=api_key, timeout=60.0, max_retries=0) as client:
            # 선택한 모델에 질문을 전달하고 응답 저장을 요청합니다.
            response = client.responses.create(
                model=model,
                input=args.prompt,
                store=True,
            )
    except AuthenticationError:
        # API 키 인증에 실패한 경우
        print("인증 오류: API 키가 유효한지 확인하세요.")
        return 1
    except RateLimitError:
        # 사용량 또는 요청 속도 한도에 걸린 경우
        print("한도 오류: API 크레딧, 사용량 한도 또는 요청 속도를 확인하세요.")
        return 1
    except APIConnectionError:
        # 연결 실패 시 서버 처리 여부가 불명확할 수 있어 Logs 확인을 안내함
        print("연결 오류: 인터넷 연결을 확인하세요. 요청 결과가 불명확하면 재실행 전 Logs를 확인하세요.")
        return 1
    except APIStatusError as error:
        # 그 밖의 API 상태 오류는 HTTP 상태 코드와 함께 안내함
        print(f"API 오류 (HTTP {error.status_code}): 모델 권한 및 프로젝트 설정을 확인하세요.")
        return 1

    # 답변 텍스트를 출력하고 텍스트가 없으면 안내 문구로 대체함
    print("AI 답변:")
    print(response.output_text or "텍스트 답변이 없습니다.")

    # 응답 ID와 상태, Logs 주소를 출력해 플랫폼에서 요청을 찾을 수 있게 함
    print(f"\n응답 ID: {response.id}")
    print(f"상태: {response.status}")
    print(f"Logs: {LOGS_URL}")
    print("API 키를 만든 조직/프로젝트를 선택하여 요청을 확인하세요.")

    return 0


if __name__ == "__main__":
    # 직접 실행할 때 main을 호출하고 반환값을 프로세스 종료 코드로 전달함
    raise SystemExit(main())
