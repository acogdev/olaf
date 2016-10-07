# Author: Gouthaman Balaraman
# http://gouthamanbalaraman.com/blog/minimal-flask-login-example.html
# http://gouthamanbalaraman.com/blog/securing-authentication-tokens.html

from flask import Flask, Response, request, render_template
from flask.ext.login import LoginManager, UserMixin, login_required
from itsdangerous import JSONWebSignatureSerializer


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


class ProtectedUser(UserMixin):
    # proxy for a database of users
    user_database = {"JohnDoe": ("JohnDoe", "John"),
                     "JaneDoe": ("JaneDoe", "Jane"),
                     'jake': ('jake', 'jake')}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls, id):
        return cls.user_database.get(id)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        jws = JSONWebSignatureSerializer(app.config["SECRET_KEY"])
        cred = jws.loads(token)

        username = cred['username']
        password = cred['password']
        user_entry = ProtectedUser.get(username)
        if (user_entry is not None):
            user = ProtectedUser(user_entry[0], user_entry[1])
            if (user.password == password):
                return user
    return None


@app.route("/", methods=["GET"])
def index():
    return Response(response="Hello World!", status=200)


@app.route("/protected/", methods=["GET"])
@login_required
def protected():
    return Response(response="Hello Protected World!", status=200)


@app.route('/token', methods=('GET', 'POST'))
def token():
    if request.method == 'GET':
        return render_template('token.html')
    else:
        jws = JSONWebSignatureSerializer(app.config["SECRET_KEY"])
        user = request.form.get('username')
        password = request.form.get('password')
        token = jws.dumps({'username': user, 'password': password})
        return token


if __name__ == '__main__':
    app.config["SECRET_KEY"] = "0439068078768605274255422272211157357409409270"
    app.run(port=7000, debug=True)
