from flask import Flask, redirect, url_for, request
from flask import render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.args)
    if request.method == 'POST':
        return "IN"
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect('/index', dat='somestring')
    return render_template('login.html')




if __name__ == '__main__':
    app.run(port=8080, debug=True)
