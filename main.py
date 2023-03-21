
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    url = request.args.get('url')
    if not url:
        return 'Error: No URL specified.'

    if request.method == 'GET':
        response = requests.get(url)
    elif request.method == 'POST':
        response = requests.post(url, data=request.form)
    elif request.method == 'PUT':
        response = requests.put(url, data=request.form)
    elif request.method == 'DELETE':
        response = requests.delete(url)
    elif request.method == 'PATCH':
        response = requests.patch(url, data=request.form)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items()
               if name.lower() not in excluded_headers]
    return response.content, response.status_code, headers
