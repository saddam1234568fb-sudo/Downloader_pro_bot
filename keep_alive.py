from flask import Flask
import threading
import logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def health_check():
    return "Bot is running beautifully.", 200

def run_flask(port):
    app.run(host='0.0.0.0', port=port)

def start_server(port=10000):
    t = threading.Thread(target=run_flask, args=(port,))
    t.daemon = True
    t.start()
