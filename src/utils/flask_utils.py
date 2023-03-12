# utils/flask_utils.py
"""
communication between client and server is always with a serialized JSON object.
Every class need to have a way to be serialized to a dict, and then to JSON
"""
import os
import requests
import json
from server import URL, ADDRESS
from flask import jsonify, request

def flask_call(method, endpoint="", data=None):
    """
    Sends a GET or POST request to the specified endpoint using Flask.

    :param method: The HTTP method to use, either 'GET' or 'POST'.
    :param endpoint: The endpoint to append to the base URL.
    :param data: A dictionary containing data to be sent with a 'POST' request.
    :return: A tuple containing a flask_response -> msg, data, status code
    """
    url = URL + endpoint
    if method == 'GET':
        resp = requests.get(url, verify=False)
        return flask_response(resp)
    elif method == 'POST':
        resp = requests.post(url, data=json.dumps({'data' : data}), verify=False)
        return flask_response(resp)
    else:
        return None, None, None

def flask_response(response):
    """
    :param response: response from flask
    :return:
    """
    return response.json()['msg'], response.json()['data'], response.status_code

def get_data():
    return json.loads(request.data)['data']

def is_folder_empty(folder):
    print(len(os.listdir(folder)))
    return len(os.listdir(folder)) == 0
