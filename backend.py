from flask import Flask, request, render_template
from threading import Thread
from flask_cors import CORS
from assistant import initAssistant, createThread, addUserMessage
import markdown2
import re

app = Flask(__name__)
CORS(app, supports_credentials=True)
assistant= initAssistant()
thread= createThread()

chatHistory=[]

@app.route("/", methods=['GET'])
def index():
  return render_template('frontEnd.html')

@app.route("/reset", methods=['GET'])
def resetChat():
  global thread
  thread= createThread()
  return "<h1>User has started a new chat</h1>"

@app.route('/sendMessage', methods=['POST'])
def runllm():
  req= request.json
  userMessage= req["message"]
  response= addUserMessage(userMessage, thread, assistant)
  html_response = markdown2.markdown(response)
  image_tagged_html_response = re.sub(r'<img ', '<img class="chat-image" ', html_response)
  #return render_template('index.html', response= image_tagged_html_response)
  return image_tagged_html_response

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=(8080))