from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to Game Store Inventory Manager 2.0!"
