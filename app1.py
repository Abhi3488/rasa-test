import os 
import threading
def actionserver():
    os.system('rasa run actions')
def endpoint():
    os.system('rasa run -m models --endpoints endpoints.yml')

def docker():
    os.system('docker run -p 8000:8000 rasa/duckling')

def api():
    os.system('rasa run --enable-api --cors "*" -p 6006')

def python():
    os.system('python3 app.py')

def mongo():
    os.system('mongo -u Abhishek -p 12345')


threading.Thread(target=actionserver).start()
threading.Thread(target=endpoint).start()
threading.Thread(target=docker).start()
threading.Thread(target=api).start()
threading.Thread(target=python).start()
threading.Thread(target=mongo).start()
