# OCI OpenAI Test

Oracle Cloud Infrastructure (OCI) Generative AI 서비스를 OpenAI API 호환 인터페이스로 사용하는 테스트 프로젝트입니다.

## 📋 목차

- [개요](#개요)
- [지원 모델](#지원-모델)
- [사전 요구사항](#사전-요구사항)
- [설치](#설치)
- [환경 설정](#환경-설정)
- [사용 방법](#사용-방법)
- [예제](#예제)
- [HTML 변환](#html-변환)
- [참고 자료](#참고-자료)

## 개요

이 프로젝트는 OCI Generative AI 서비스를 OpenAI API와 호환되는 방식으로 사용하는 방법을 보여줍니다. `oci-openai` 패키지를 사용하여 다양한 LLM 모델에 접근할 수 있습니다.

## 지원 모델

다음 모델들을 사용할 수 있습니다:

- **xAI Grok 시리즈**
  - `xai.grok-4-fast-reasoning`
  - `xai.grok-4-fast-non-reasoning`
  - `xai.grok-4`
  - `xai.grok-3`
  - `xai.grok-3-fast`

- **Cohere 모델** (지원안함)
  - `cohere.command-a-03-2025`
  - `cohere.embed-v4.0`

- **Meta Llama 모델**
  - `meta.llama-4-scout-17b-16e-instruct`

- **Google Gemini 모델**(지원안함)
  - `google.gemini-2.5-pro`
  - `google.gemini-2.5-flash`
  - `google.gemini-2.5-flash-lite`

## 사전 요구사항

- Python 3.12 이상
- OCI 계정 및 적절한 권한
- OCI CLI 설정 완료 (프로파일 구성)
- Compartment ID

## 설치

### 1. 저장소 클론

```bash
git clone https://github.com/hiwylee/oci-openai-test.git
cd oci-openai-test
```

### 2. 의존성 설치

이 프로젝트는 `uv` 패키지 매니저를 사용합니다:

```bash
# uv가 설치되어 있지 않다면
curl -LsSf https://astral.sh/uv/install.sh | sh

# 의존성 설치
uv sync
```

또는 pip를 사용하는 경우:

```bash
uv pip install oci-openai langchain-openai python-dotenv
```

## 환경 설정

### 1. 환경 변수 파일 생성

`env.examples` 파일을 참고하여 `.env` 파일을 생성합니다:

```bash
cp env.examples .env
```

### 2. `.env` 파일 수정

```env
compartment_id=ocid1.compartment.oc1..your_compartment_id
profile_name=your_profile_name
region=us-chicago-1
```

**설정 항목 설명:**
- `compartment_id`: OCI Compartment OCID
- `profile_name`: OCI CLI 프로파일 이름
- `region`: OCI 리전 (예: us-chicago-1)

## 사용 방법

### 방법 1: OciOpenAI 클라이언트 사용

```python
from oci_openai import OciOpenAI, OciUserPrincipalAuth

client = OciOpenAI(
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    auth=OciUserPrincipalAuth(profile_name="your_profile"),
    compartment_id="your_compartment_id",
)

completion = client.chat.completions.create(
    model="xai.grok-4-fast-non-reasoning",
    messages=[
        {
            "role": "user",
            "content": "안녕하세요!",
        },
    ],
)
print(completion.model_dump_json())
```

### 방법 2: OpenAI 클라이언트 사용

```python
import httpx
from openai import OpenAI
from oci_openai import OciUserPrincipalAuth

client = OpenAI(
    api_key="OCI",
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
    http_client=httpx.Client(
        auth=OciUserPrincipalAuth(profile_name="your_profile"), 
        headers={"CompartmentId": "your_compartment_id"}
    ),
)

response = client.chat.completions.create(
    model="xai.grok-4-fast-non-reasoning",
    messages=[
        {
            "role": "user",
            "content": "안녕하세요!",
        },
    ],
)
print(response.model_dump_json())
```

### 방법 3: LangChain 통합

```python
from langchain_openai import ChatOpenAI
import httpx
from oci_openai import OciUserPrincipalAuth

llm = ChatOpenAI(
    model="xai.grok-4-fast-reasoning",
    api_key="OCI",
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
    http_client=httpx.Client(
        auth=OciUserPrincipalAuth(profile_name="your_profile"), 
        headers={"CompartmentId": "your_compartment_id"}
    ),
)

messages = [
    ("system", "You are a helpful assistant."),
    ("human", "안녕하세요!"),
]
ai_msg = llm.invoke(messages)
print(ai_msg)
```

## 예제

### 실행

```bash
# Python 스크립트 실행
uv run python main.py

# 또는 Jupyter Notebook 사용
uv run jupyter notebook oci-openai.ipynb
```

## HTML 변환

Jupyter Notebook을 HTML로 변환하려면:

```bash
# nbconvert 설치 (아직 설치하지 않은 경우)
uv add jupyter nbconvert

# HTML로 변환
uv run jupyter nbconvert --to html oci-openai.ipynb
```

변환된 HTML 파일은 `oci-openai.html`로 생성됩니다.

## 인증 방법

`oci-openai` 패키지는 다양한 인증 방법을 지원합니다:

- `OciUserPrincipalAuth`: 사용자 프린시펄 인증 (기본)
- `OciSessionAuth`: 세션 기반 인증
- `OciResourcePrincipalAuth`: 리소스 프린시펄 인증
- `OciInstancePrincipalAuth`: 인스턴스 프린시펄 인증

## 프로젝트 구조

```
oci-openai-test/
├── .env                    # 환경 변수 (git에서 제외됨)
├── .gitignore             # Git 제외 파일 목록
├── env.examples           # 환경 변수 예제
├── main.py                # 메인 Python 스크립트
├── oci-openai.ipynb       # Jupyter Notebook
├── oci-openai.html        # 변환된 HTML 파일
├── pyproject.toml         # 프로젝트 설정
└── README.md              # 이 파일
```

## 참고 자료

- **공식 문서**: [https://github.com/hiwylee/oci-openai](https://github.com/hiwylee/oci-openai)
- **PyPI 패키지**: [oci-openai](https://pypi.org/project/oci-openai/)
- **OCI Generative AI 문서**: [Oracle Cloud Infrastructure Documentation](https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm)

## 라이선스

이 프로젝트는 테스트 목적으로 작성되었습니다.

## 문제 해결

### OCI 인증 오류
- OCI CLI가 올바르게 설정되어 있는지 확인하세요
- `~/.oci/config` 파일에 프로파일이 존재하는지 확인하세요

### Compartment ID 오류
- `.env` 파일의 `compartment_id`가 올바른지 확인하세요
- OCI 콘솔에서 Compartment OCID를 복사하세요

### 모델 접근 오류
- 해당 리전에서 모델이 사용 가능한지 확인하세요
- Compartment에 적절한 권한이 있는지 확인하세요
