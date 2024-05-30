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
        { "role": "system", "content": "You are an assistant for web developers. You provide working source code based in the requirements of the developers. When they ask you to generate source files your answer must be only the file content, don't add any explanation, instructions or whatever and don't wrap it in markdown, just output the file content." },
        { "role": "user", "content": [  
            { 
                "type": "text", 
                "text": "I need the HTML and CSS files to create a web page based in this image. Please, first generate only the HTML file." 
            },
            { 
                "type": "image_url",
                "image_url": {
                    "url": url
                }
            }
        ] } 
    ]

css_message = { "role": "user", "content": "Now please generate only the CSS file." }

response = client.chat.completions.create(
        model=deployment,
        messages = messages,
        temperature=0.99,
        max_tokens=800
    )

print(response.choices[0].message.content)

messages.append(response.choices[0].message)
messages.append(css_message)

response = client.chat.completions.create(
        model=deployment,
        messages = messages,
        temperature=0.99,
        max_tokens=800
    )

print(response.choices[0].message.content)
