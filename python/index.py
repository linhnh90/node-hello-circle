from flask import Flask
import os

hostname = os.getenv('HOSTNAME', "unknow")
app_version = os.getenv('APP_VERSION', "unknow")
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello Python! Application version " + app_version + "--Enviroment " + hostname
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
