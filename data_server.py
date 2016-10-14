from flask import Flask, url_for, session, request, jsonify
from requests_oauthlib import OAuth2Session
import os
import ast


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'


app = Flask(__name__)
app.secret_key = 'secrsljkglsdfuyrevbnksjflkset'


@app.route('/')
def index():
    token = request.headers.get('token')
    if token is None:
        token = request.args.get('token')
    try:
        TOKEN = ast.literal_eval(token)

        SESSION = OAuth2Session(token=TOKEN)
        r = SESSION.get('http://localhost:5000/api/me')
        if r.status_code == 200:
            return '\n data_server accessed with token\n'

        return ''

    except Exception as e:
        print(e)
        return(str(e))



if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=8000)
