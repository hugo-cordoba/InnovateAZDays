import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

deployment = os.getenv["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]

response = client.chat.completions.create(
        model=deployment,
        messages = 'Write a tagline for an ice cream shop',
        temperature=0.7,
        max_tokens=800
    )
