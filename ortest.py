
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider 

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
   
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  
   
client = AzureOpenAI(
  azure_endpoint = endpoint,
  azure_ad_token_provider=token_provider,
  api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
)

response = client.chat.completions.create(
    model=os.getenv("DEPLOYMENT_NAME", "gpt5"),
    messages=[
        # The new 'o1mini' model does not support the system role. Please remove the following line if you are using the new 'o1mini' model.
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)