import os
import json
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version = "2024-02-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

def call_openai_and_write_file(messages, file_name=""):
    response = client.chat.completions.create(
        model = os.getenv("CHAT_COMPLETIONS_DEPLOYMENT_NAME"),
        messages = messages,
        temperature = 0.0001,
        max_tokens = 4000
    )

    file_content = ""

    if not file_name:
        file_json = json.loads(response.choices[0].message.content, strict=False)
        file_content = file_json['filecontent']
        file_name = "temp/" + file_json['filename']
    else:
        file_content = response.choices[0].message.content

    print(file_content)

    with open(file_name, 'w') as f:
        f.write(file_content)

    return response.choices[0].message

def get_url(file):
    with open(file) as f:
        issue_body = f.read()
        return issue_body.split("](")[1].split(")")[0]

def get_appname(file):
    appname = ""
    with open(file) as f:
        appname = f.read().split("App:")[1].strip().replace(" ", "").lower()
    with open("temp/appname.txt", 'w') as f:
        f.write(appname)
    return appname

appname = get_appname('temp/title.txt')
url = get_url('temp/body.txt')


print("🚀🚀🚀 GENERATING SUMMARY 🚀🚀🚀")

messages=[
    { "role": "system", "content": "You are an assistant for web developers. You provide working source code based on image sketches." },
    { "role": "user", "content": [  
        { 
            "type": "text", 
            "text": f"Based on this image, generate a markdown file describing the files that would be generated for a new standalone angular component named '{appname}' for this app. These include: model, service to call the backend REST API, component logic, html and css. Do not include source code, just a summary of the component and the files. Include in the summary an OpenAPI specification in YAML that describes the necessary API for this component. Don't wrap this json in markdown." 
        },
        { 
            "type": "image_url",
            "image_url": { "url": url }
        }
    ] }
]

response = call_openai_and_write_file(messages, 'temp/summary.md')

print("🚀🚀🚀 GENERATING API SPEC 🚀🚀🚀")

messages.append(response)
messages.append({ "role": "user", "content": "Show me the same OpenAPI specification in YAML again. Don't wrap this json in markdown." })
response = call_openai_and_write_file(messages, f"temp/{appname}.yml")

print("🚀🚀🚀 GENERATING MODEL 🚀🚀🚀")

messages.append(response)
messages.append({ "role": "user", "content": "Generate the component model implementation file. Reply with the source code formatted inside a json with two keys: 'filename' and 'filecontent'. Don't wrap this json in markdown." })
response = call_openai_and_write_file(messages)

print("🚀🚀🚀 GENERATING SERVICE 🚀🚀🚀")
messages.append(response)
messages.append({ "role": "user", "content": "Generate the component service implementation file to call the backend REST API. Reply with the source code formatted inside a json with two keys: 'filename' and 'filecontent'. Don't wrap this json in markdown." })
response = call_openai_and_write_file(messages)

print("🚀🚀🚀 GENERATING HTML 🚀🚀🚀")
messages.append(response)
messages.append({ "role": "user", "content": "Generate the component html implementation file. Reply with the source code formatted inside a json with two keys: 'filename' and 'filecontent'. Don't wrap this json in markdown." })
response = call_openai_and_write_file(messages)

print("🚀🚀🚀 GENERATING CSS 🚀🚀🚀")
messages.append(response)
messages.append({ "role": "user", "content": "Generate the component css implementation file. Reply with the source code formatted inside a json with two keys: 'filename' and 'filecontent'. Don't wrap this json in markdown." })
response = call_openai_and_write_file(messages)

print("🚀🚀🚀 GENERATING COMPONENT 🚀🚀🚀")
messages.append(response)
messages.append({ "role": "user", "content": "Generate the standalone angular component logic implementation file (standalone: true). Reply with the source code formatted inside a json with two keys: 'filename' and 'filecontent'. Don't wrap this json in markdown." })
response = call_openai_and_write_file(messages)