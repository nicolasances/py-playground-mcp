"""
Azure OpenAI with Microsoft Entra ID Authentication Demo

This script demonstrates different approaches to authenticate and call Azure OpenAI
using Microsoft Entra ID (formerly Azure AD) authentication with your user account.

Prerequisites:
    pip install azure-identity openai langchain-openai requests python-dotenv

Authentication:
    Uses DefaultAzureCredential which will authenticate using your logged-in Azure CLI
    or Visual Studio Code credentials.
"""

import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "gpt5")


def example_1_raw_requests():
    """
    Example 1: Using raw requests library with Microsoft Entra ID token
    """
    print("\n=== Example 1: Raw Requests with Entra ID ===")
    
    # Get credentials using DefaultAzureCredential
    # This will use your logged-in Azure CLI or VS Code credentials
    credential = DefaultAzureCredential()
    
    # Get token for Azure Cognitive Services
    # The scope should be for Cognitive Services
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    
    # Prepare the request
    url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"
    
    headers = {
        "Authorization": f"Bearer {token.token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is Azure OpenAI?"}
        ],
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        print(f"Response: {result['choices'][0]['message']['content']}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")


def example_2_openai_sdk():
    """
    Example 2: Using OpenAI Python SDK with Azure and Entra ID
    """
    print("\n=== Example 2: OpenAI SDK with Entra ID ===")
    
    try:
        from openai import AzureOpenAI
        
        # Get token provider for Azure Cognitive Services
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credential,
            "https://cognitiveservices.azure.com/.default"
        )
        
        # Create Azure OpenAI client with Entra ID authentication
        client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            azure_ad_token_provider=token_provider,
            api_version=AZURE_OPENAI_API_VERSION
        )
        
        # Make a chat completion request
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Explain Microsoft Entra ID in one sentence."}
            ],
        )
        
        print(f"Response: {response.choices[0].message.content}")
        
    except ImportError:
        print("OpenAI SDK not installed. Run: pip install openai")
    except Exception as e:
        print(f"Error: {e}")


def example_3_langchain():
    """
    Example 3: Using LangChain with Azure OpenAI and Entra ID
    """
    print("\n=== Example 3: LangChain with Entra ID ===")
    
    try:
        from langchain_openai import AzureChatOpenAI
        
        # Get token provider for Azure Cognitive Services
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credential,
            "https://cognitiveservices.azure.com/.default"
        )
        
        # Create LangChain Azure OpenAI instance
        llm = AzureChatOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            azure_deployment=DEPLOYMENT_NAME,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_ad_token_provider=token_provider
        )
        
        # Invoke the model
        response = llm.invoke("What are the benefits of using Azure OpenAI?")
        print(f"Response: {response.content}")
        
    except ImportError:
        print("LangChain not installed. Run: pip install langchain-openai")
    except Exception as e:
        print(f"Error: {e}")


def example_4_streaming():
    """
    Example 4: Streaming responses with OpenAI SDK and Entra ID
    """
    print("\n=== Example 4: Streaming with Entra ID ===")
    
    try:
        from openai import AzureOpenAI
        
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credential,
            "https://cognitiveservices.azure.com/.default"
        )
        
        client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            azure_ad_token_provider=token_provider,
            api_version=AZURE_OPENAI_API_VERSION
        )
        
        # Stream the response
        print("Streaming response: ", end="", flush=True)
        stream = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "user", "content": "Count from 1 to 5."}
            ],
            stream=True,
        )
        
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print()  # New line after streaming
        
    except ImportError:
        print("OpenAI SDK not installed. Run: pip install openai")
    except Exception as e:
        print(f"Error: {e}")


def check_authentication():
    """
    Check if Azure authentication is properly configured
    """
    print("\n=== Checking Azure Authentication ===")
    
    try:
        credential = DefaultAzureCredential()
        token = credential.get_token("https://cognitiveservices.azure.com/.default")
        print("✓ Successfully obtained authentication token")
        print(f"✓ Token expires at: {token.expires_on}")
        return True
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        print("\nMake sure you're logged in via Azure CLI:")
        print("  az login")
        return False


if __name__ == "__main__":
    print("Azure OpenAI with Microsoft Entra ID Authentication Demo")
    print("=" * 60)
    
    # First, verify authentication
    if not check_authentication():
        print("\nPlease authenticate first and try again.")
        exit(1)
    
    print(f"\nEndpoint: {AZURE_OPENAI_ENDPOINT}")
    print(f"Deployment: {DEPLOYMENT_NAME}")
    print("\nNote: Update DEPLOYMENT_NAME with your actual deployment name!")
    
    # Run examples
    # Uncomment the examples you want to run:
    
    # example_1_raw_requests()
    # example_2_openai_sdk()
    # example_3_langchain()
    example_4_streaming()
    
    print("\n" + "=" * 60)
    print("Demo completed!")
