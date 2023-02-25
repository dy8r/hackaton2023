from flask import Flask, jsonify, request, session
from flask_restful import Api, Resource
from datetime import datetime, timedelta
from functools import wraps
import json
import time
from dateutil import parser
import os
from time import sleep
import requests
from flask_cors import CORS
from gpt import send_request_to_openai

app = Flask(__name__)
api = Api(app)
CORS(app)


class TextOne(Resource):
    def post(self):
        try:
            req = request.get_json()
            print(req)
            prompt = req['text']
            response = send_request_to_openai(prompt)
            print(response)
            return {"status": "success", 'response': response}
        except Exception as e:
            print(e)
            return {'status': str(e)}
        
class TextTwo(Resource):
    def post(self):
        try:

            return {"status": "success"}
        except Exception as e:
            print(e)
            return {'status': str(e)}
        
class TextThree(Resource):
    def post(self):
        try:

            return {"status": "success"}
        except Exception as e:
            print(e)
            return {'status': str(e)}

api.add_resource(TextOne, "/text1/")
api.add_resource(TextTwo, "/text2/")
api.add_resource(TextThree, "/text3/")

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 80, debug = False)
    # app.run(debug = True)
