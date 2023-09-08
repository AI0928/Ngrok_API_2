# API_demo
import os
from flask import Flask, request, jsonify
from pyngrok import ngrok, conf
import json
from recomend import *

# ngrokトークンを設定(ngrokの自分のアカウントページからコピペ)
conf.get_default().auth_token = "****************"

app = Flask(__name__)

# 日本語を使えるように
app.config['JSON_AS_ASCII'] = False

@app.route("/")
def home():
    return "<h1>Hello World!</h1>"

@app.route("/api/recommendfood/<string:target_user>")
def getRecommendFood(target_user):
    return recommend_food(target_user)


@app.route("/api/employeematche/<string:employee_id>")
def getRecommendMatche(employee_id):
    return recommend_matche(employee_id)

if __name__ == "__main__":
    public_url = ngrok.connect(5000)
    print(f"ngrok URL: {public_url}")
    app.run(port=5000)
