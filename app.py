from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def echo():
    if request.method == 'GET':
        return "Hello! I will echo whatever you send me!"
    elif request.method == 'POST':
        return request.data

if __name__ == "__main__":
    app.run()