import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

deployment = os.getenv("CHAT_COMPLETIONS_DEPLOYMENT_NAME")

def call_openai(messages):
    response = client.chat.completions.create(
        model=deployment,
        messages = messages,
        temperature=0.99,
        max_tokens=800
    )
    print(response.choices[0].message.content)
    return response.choices[0].message

def write_file(file_name, content):
    with open(file_name, 'w') as f:
        f.write(content)

def get_url(file):
    with open(file) as f:
        issue_body = f.read()
        if "](https://" in issue_body:
            url = issue_body.split("](")[1].split(")")[0]
            return url
        else:
            return None

url = get_url('temp/body.txt')
print(f'URL: {url}

messages=[
        { "role": "system", "content": "You are an assistant for web developers. You provide working source code based in image sketches. All your answers must be limited to output the generated file content. Don't add any explanation, instruction, or any markdown to the answer. Don't wrap the answer in markdown. Just output the genreated file content." },
        { "role": "user", "content": [  
            { 
                "type": "text", 
                "text": "I am creating an Angular project. I have already run the 'ng new' command and know I need the 'index.html', 'styles.css' and 'main.ts' files to create a web page based in this image. Please, first generate only the 'index.html' file." 
            },
            { 
                "type": "image_url",
                "image_url": {
                    "url": url
                }
            }
        ] } 
    ]

css_message = { "role": "user", "content": "Now please generate only the 'styles.css' file." }
ts_message = { "role": "user", "content": "And finally please generate only the 'main.ts' file." }

response = call_openai(messages)
write_file('temp/index.html', response.content)

messages.append(response)
messages.append(css_message)

response = call_openai(messages)
write_file('temp/styles.css', response.content)

messages.append(response)
messages.append(ts_message)

response = call_openai(messages)
write_file('temp/main.ts', response.content)
