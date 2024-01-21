from flask import Flask, request, render_template, url_for, redirect
from flask_cors import CORS
from assistant import initAssistant, createThread, addUserMessage, getMessages
import markdown2
import re

app = Flask(__name__)
CORS(app, supports_credentials=True)

assistant= initAssistant()
thread= createThread()
chatHistory=[]

@app.route("/", methods=['GET'])
def index():
  reset_status = 'resetStatus' in request.args
  return render_template('frontEnd.html', resetStatus=reset_status)

@app.route("/reset", methods=['GET'])
def resetChat():
  global thread
  thread= createThread()
  global chatHistory
  chatHistory=[]
  return redirect(url_for('index', resetStatus=True))

@app.route('/sendMessage', methods=['POST'])
def runllm():
  req= request.json
  userMessage= req["message"]
  response= addUserMessage(userMessage, thread, assistant)
  html_response = markdown2.markdown(response)
  image_tagged_html_response = re.sub(r'<img ', '<img class="chat-image" ', html_response)
  chatInstance={}
  chatInstance["User"]=userMessage
  chatInstance["Bot"]=image_tagged_html_response
  chatHistory.append(chatInstance)
  return chatHistory

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=(8080))