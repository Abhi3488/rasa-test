from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
import os, sys, requests, json
from random import randint
# from flask_lt import run_with_lt
# from pyngrok import ngrok

app = Flask(__name__)
# run_with_lt(app)
# ngrok.set_auth_token("28jg4mG15wFkeqtc050Lq4KcmvR_4w9K3Q4242xYya5USFv9q")

# public_url = ngrok.connect(5000).public_url

# print(public_url)


conn = MongoClient('mongodb://localhost:27017')
db = conn['rasa']
coll = db['user']



@app.route('/')
def home():
    return render_template("index.html")
#    return "Hello from flask api"

@app.route('/parse', methods = ['GET'])
def extract():

    #text = str(request.form.get('value1'))                                                                                                                                                                
    text = str(request.args.get("text"))
    sessionID = str(request.args.get("sessionID"))
    #text="hello"                                                                                                                                                                            
    #sessionID = "RASA3"                                                                                                                                                                                   
    #text = "Book an appointment"                                                                                                                                                                          
    app.logger.info('sessionID: %s',sessionID)
    app.logger.info('TEXT: %s',text)
    payload = json.dumps({"sender":sessionID,"message":text})
    headers = {'Content-type':'application/json', 'Accept':'text/plain'}
    response = requests.request("POST",url="http://localhost:5005/webhooks/rest/webhook", headers= headers, data = payload)

    response = response.json()
    app.logger.info('--RESPONSE: %s',response)
    resp = []
    app.logger.info('--len(response): %s',len(response))
    for i in range(len(response)):
        try:
            msg=response[i]['text']
            resp.append(response[i]['text'])

        except:
            continue
    result = resp
    app.logger.info('--result = %s', result)
    return str(msg)

if __name__ == "__main__":
    app.run()

