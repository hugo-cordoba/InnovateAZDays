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
        temperature=0.1,
        max_tokens=4000
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

def get_appname(file):
    with open(file) as f:
        issue_title = f.read()
        if "App:" in issue_title:
            appname = issue_title.split("App:")[1].strip().replace(" ", "").lower()
            return appname
        else:
            return None

appname = get_appname('temp/title.txt')
print(appname)

url = get_url('temp/body.txt')
print(url)

messages=[
        { "role": "system", "content": "You are an assistant for web developers. You provide working source code based in image sketches." },
        { "role": "user", "content": [  
            { 
                "type": "text", 
                "text": f"Based in this image, generate a markdown with the files that would be generated for a new standalone angular component named '{appname}' for this app. These include: model, service, component logic, html and css. Do not include source code, just a summary of the application and the files. Include in the summary an OpenAPI specification in YAML that describes the necessary API for this app. Reply with the markdown source code only. Don't wrap the answer in markdown." 
            },
            { 
                "type": "image_url",
                "image_url": {
                    "url": url
                }
            }
        ] } 
    ]

model_message = { "role": "user", "content": "Generate the component model implementation file. Reply with the source code only. Don't wrap the answer in markdown." }
service_message = { "role": "user", "content": "Generate the component service implementation file. Reply with the source code only. Don't wrap the answer in markdown." }
logic_message = { "role": "user", "content": "Generate the component logic implementation file. Reply with the source code only. Don't wrap the answer in markdown." }
html_message = { "role": "user", "content": "Generate the component html implementation file. Reply with the source code only. Don't wrap the answer in markdown." }
css_message = { "role": "user", "content": "Generate the component css implementation file. Reply with the source code only. Don't wrap the answer in markdown." }

response = call_openai(messages)
write_file('temp/summary.md', response.content)

messages.append(response)
messages.append(model_message)

response = call_openai(messages)
write_file(f'temp/{appname}.model.ts', response.content)

messages.append(response)
messages.append(service_message)

response = call_openai(messages)
write_file(f'temp/{appname}.service.ts', response.content)

messages.append(response)
messages.append(logic_message)

response = call_openai(messages)
write_file(f'temp/{appname}.component.ts', response.content)

messages.append(response)
messages.append(html_message)

response = call_openai(messages)
write_file(f'temp/{appname}.component.html', response.content)

messages.append(response)
messages.append(css_message)

response = call_openai(messages)
write_file(f'temp/{appname}.component.css', response.content)
