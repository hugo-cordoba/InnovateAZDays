import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

deployment = os.getenv("CHAT_COMPLETIONS_DEPLOYMENT_NAME")

messages = [{"role": "system", "content": "You are a HELPFUL assistant answering users questions. Answer in a clear and concise manner."},
            {"role": "user", "content": "Write a tagline for an ice cream shop"}]

response = client.chat.completions.create(
        model=deployment,
        messages = messages,
        temperature=0.99,
        max_tokens=800
    )

print(response.choices[0].message.content)