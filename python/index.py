from flask import Flask
import os

app_env = os.getenv('APP_ENV')
app_version = os.getenv('APP_VERSION')
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello World! Application version" + app_version "--Enviroment" + app_env
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
