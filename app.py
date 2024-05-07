from flask import Flask, render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.bd'
db = SQLAlchemy(app)



@app.route('/')
def index():  # put application's code here
    return render_template('signINUP.html')


if __name__ == '__main__':
    app.run(debug=True)
