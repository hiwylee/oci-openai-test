
# %% [markdown]
### 참조 문서
# %% [markdown]
### 참조 문서
# - Docs: [htps://github.com/hiwylee/oci-openai](https://github.com/hiwylee/oci-openai)
# - Package: [oci-openai](https://pypi.org/project/oci-openai/)
# ```
# uv add oci-openai
# ```
# - .env
# ```
# region=us-chicago-1
# profile_name=chicago
# compartment_id=ocid1.compartment.oc1..xlpl4x6rdgv3ak3egq
# ```
### 샐행 결과 html 로 변환
# ```
# uv add jupyter nbconvert 
# uv run jupyter nbconvert --to html oci-openai.ipynb
# ```

# %%
import os
from dotenv import load_dotenv
load_dotenv(override=True)

region = os.getenv("region",)
compartment_id = os.getenv("compartment_id")
profile_name = os.getenv("profile_name")
service_endpoint=f"https://inference.generativeai.{region}.oci.oraclecloud.com",

# %%
print(f"regin={region}, profile={profile_name}\nservice_endpoint={service_endpoint}")

# %%    

from oci_openai import OciOpenAI, OciUserPrincipalAuth

client = OciOpenAI(
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    #auth=OciSessionAuth(profile_name=profile_name),
    #auth=OciResourcePrincipalAuth(profile_name=profile_name),
    #auth=OciInstancePrincipalAuth(profile_name=profile_name),
    auth=OciUserPrincipalAuth(profile_name=profile_name),
    compartment_id=compartment_id,
)
models = [
    "xai.grok-4-fast-reasoning",
    "xai.grok-4-fast-non-reasoning",
    "xai.grok-4",
    "xai.grok-3",
    "xai.grok-3-fast",
    "cohere.command-a-03-2025",
    "cohere.embed-v4.0",
    "meta.llama-4-scout-17b-16e-instruct",
    "google.gemini-2.5-pro",
    "google.gemini-2.5-flash",
    "google.gemini-2.5-flash-lite",
    "meta.llama-4-scout-17b-16e-instruct"
]


model = "xai.grok-4-fast-non-reasoning"
completion = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "오늘 AI news를 용약해줘?",
        },
    ],
)
print(completion.model_dump_json())


# %%
import httpx
from openai import OpenAI
from oci_openai import OciUserPrincipalAuth

# Example for OCI Data Science Model Deployment endpoint
client = OpenAI(
    api_key="OCI",
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
    http_client=httpx.Client(
        auth=OciUserPrincipalAuth(profile_name=profile_name), 
        headers={"CompartmentId": compartment_id}
    ),
)

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "오늘 AI news를 요약해줘?",
        },
    ],
)
print(response.model_dump_json())

#%%
from langchain_openai import ChatOpenAI
import httpx
from oci_openai import OciUserPrincipalAuth
import os


COMPARTMENT_ID=compartment_id

llm = ChatOpenAI(
    model=model,  # for example "xai.grok-4-fast-reasoning"
    api_key="OCI",
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
    http_client=httpx.Client(
        auth=OciUserPrincipalAuth(profile_name=profile_name ), 
        headers={"CompartmentId": COMPARTMENT_ID}
    ),
    # use_responses_api=True
    # stream_usage=True,
    # temperature=None,
    # max_tokens=None,
    # timeout=None,
    # reasoning_effort="low",
    # max_retries=2,
    # other params...
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg)
