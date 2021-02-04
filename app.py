from flask import Flask

app = Flask(__name__)

@app.route('/')
def echo():
    return "Hello! I don't echo yet :)"

if __name__ == "__main__":
    app.run()