import requests
import os   
import time
from openai import OpenAI
from dotenv import load_dotenv
#TODO manage message history

load_dotenv()
OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')
CAT_API_KEY= os.getenv('CAT_API_KEY')
client = OpenAI()


headers = {
'Authorization': "Bearer {}".format(OPENAI_API_KEY),
"OpenAI-Beta": "assistants=v1"
}


assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo-1106"
)


thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What is 1+1. Can you help me?"
)

#print(message)
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)

def catCall(data):
    print("cat called")
    functionCallInfo= data["required_action"]["submit_tool_outputs"]["tool_calls"][0]
    print(functionCallInfo)
    callId=functionCallInfo["id"]
    funcName=functionCallInfo["function"]["name"]
    funcParam=functionCallInfo["function"]["arguments"]
    return
def completed():
    print("completed")
    return

while True:
    print("polling")
    r= requests.get("https://api.openai.com/v1/threads/{}/runs/{}".format(thread.id,run.id), headers=headers)
    data = r.json()
    status= data["status"]
    if status=="requires_action":
        catCall(data)
        break
    elif status=="completed":
        completed()
        break

    elif status=="queued" or status=="in_progress":
        print("in progress")
        time.sleep(1)
    else:
        print(status)
        break
        

def get_response(thread):
    messages = client.beta.threads.messages.list(thread_id=thread.id, order="desc", limit=1)
    last_message = messages.data[0].content[0].text.value
    return last_message

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(messages.data[0].id)
print(get_response(thread))