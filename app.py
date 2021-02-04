from flask import Flask, request, Response
from os import environ


app = Flask(__name__)
app.config['SERVER_KEY'] = environ.get("SERVER_KEY")


def check_auth(f):
    def wrapper(*args, **kwargs):
        try:
            if request.headers['server_key'] != app.config['SERVER_KEY']:
                return Response("Incorrect server key", status=403)
            return f(*args, **kwargs)
        except KeyError:
            return Response("Please add server_key to access", status=403)
    return wrapper


@app.route('/', methods=["GET", "POST"])
@check_auth
def echo():
    """Echos back what is sent to it when accessed with Server Key"""
    if request.method == 'GET':
        return "Hello! I will echo whatever you send me!"
    if request.method == 'POST':
        return request.data

if __name__ == "__main__":
    app.run()
