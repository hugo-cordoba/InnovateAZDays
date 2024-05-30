import os
import re
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

deployment = os.getenv("CHAT_COMPLETIONS_DEPLOYMENT_NAME")

with open('temp/body.txt') as f:
    issue_body = f.read()
    if "](https://" in issue_body:
        url = issue_body.split("](")[1].split(")")[0]
        print(url)
    else:
        print("No image found")
        quit()

messages=[
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": [  
            { 
                "type": "text", 
                "text": "Describe this picture:" 
            },
            { 
                "type": "image_url",
                "image_url": {
                    "url": url
                }
            }
        ] } 
    ]

response = client.chat.completions.create(
        model=deployment,
        messages = messages,
        temperature=0.99,
        max_tokens=800
    )

print(response.choices[0].message.content)