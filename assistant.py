import requests
import os   
import time
from openai import OpenAI
from dotenv import load_dotenv
import json
from catCalling import getCatPictureAdv

load_dotenv()
OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')
CAT_API_KEY= os.getenv('CAT_API_KEY')
client = OpenAI()


headers = {
'Authorization': "Bearer {}".format(OPENAI_API_KEY),
"OpenAI-Beta": "assistants=v1"
}

def initAssistant():
    assistant = client.beta.assistants.create(
    instructions="You are a cat chatbot who provides cat pictures to employees of Nika.eco. Use the provided functions to render your services.",
    model="gpt-4-1106-preview",
    tools=[{
        "type": "function",
        "function": {
            "name": "getCatPictureAdv",
            "description": "Get pictures of cats based on specified criteria",
            "parameters": {
            "type": "object",
            "properties": {
                "quantity": {
                "type": "integer",
                "description": "Number of cat pictures to retrieve"
                },
                "diff_breeds": {
                "type": "boolean",
                "description": "Whether to get different breeds (true) or same breed (false)"
                }
            },
            "required": ["quantity"]
            }
        }
    }]
    )
    return assistant
def createThread():
    thread = client.beta.threads.create()
    return thread

def catCall(data,thread, run):
    print("cat called")
    functionCallInfo= data["required_action"]["submit_tool_outputs"]["tool_calls"][0]
    callId=functionCallInfo["id"]
    funcName=functionCallInfo["function"]["name"]
    funcParam=json.loads(functionCallInfo["function"]["arguments"])
    funcOutput= json.dumps(globals()[funcName](**funcParam))
    #funcOutput= json.dumps(globals()[funcName]())
    print(funcOutput)
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=[
            {
                "tool_call_id": callId,
                "output": funcOutput,
            }
            ]
    )
    return processAIResponse(thread, run)


def get_response(thread):
    messages = client.beta.threads.messages.list(thread_id=thread.id, order="desc", limit=1)
    last_message = messages.data[0].content[0].text.value
    return last_message


def finish_response(thread): #TODO send back to frontend-> AI message + chat history
    print("AI's Response")
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(messages.data[0].content[0].text.value)
    return messages.data[0].content[0].text.value
    

def processAIResponse(thread, run):
    while True:
        print("polling")
        r= requests.get("https://api.openai.com/v1/threads/{}/runs/{}".format(thread.id,run.id), headers=headers)
        data = r.json()
        status= data["status"]
        if status=="requires_action":
            return catCall(data,thread, run)
        elif status=="completed":
            return finish_response(thread)
        elif status=="queued" or status=="in_progress":
            print("in progress")
            time.sleep(1)
        else:
            print(status)
            print("unhandled status")
            return None

def addUserMessage(msg, thread,assistant):
    print("User's Message "+ msg)
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=msg
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Be pleasant and encourage users with pictures of cats."
    )
    return processAIResponse(thread, run)

if __name__=="__main__":
   assistant= initAssistant()
   thread=createThread()
   print(addUserMessage("I am feeling burnt out, could you help me?", thread, assistant))
   print(addUserMessage("I would like to have 3 cat pictures of different species. Can you help me?", thread, assistant))