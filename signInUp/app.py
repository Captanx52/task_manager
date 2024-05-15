from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class USER(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<USER %r>' % self.id


@app.route('/sign_up', methods=['POST', 'GET'])
def signup():  # put application's code here
    if request.method == 'POST':
        username_n = request.form['username']
        email = request.form['email']
        password_n = request.form['password']

        password_str = ''.join(str(ord(char)) for char in password_n) + '2201'
        password_int = int(password_str)

        username_str = ''.join(str(ord(char)) for char in username_n) + '108102108'
        username_int = int(username_str)

        password = password_int ^ username_int

        print(password)
        if password_n == None:
            error = 'Please enter a password'
            return render_template('signin.html', error=error)
        else:
            new_user = USER(username=username_n, email=email, password=str(password))
            db.session.add(new_user)
            db.session.commit()
            return redirect('/sign_in')

    else:
        return render_template('signUp.html', methods=['POST', 'GET'])


@app.route('/sign_in', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username_n = request.form['username']
        password_n = request.form['password']

        password_str = ''.join(str(ord(char)) for char in password_n) + '2201'
        password_int = int(password_str)

        username_str = ''.join(str(ord(char)) for char in username_n) + '108102108'
        username_int = int(username_str)

        password = password_int ^ username_int



        print(len(str(password)))
        user = USER.query.filter_by(username=username_n).first()
        if user == None:
            error = 'User not found!'
            return render_template('signIn.html.html', error=error)
        if user.password == str(password) :
            return password
        else:
            error = 'Password is wrong!'
            return render_template('signIn.html', error=error)
    else:
        return render_template('signIn.html')



if __name__ == '__main__':
    app.run(debug=True)
