# web server hosting the bot
# https://repl.it/talk/learn/package-operation-failed/11008/129067

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return 'Bot ready!'

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()