from flask import Flask, render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.id


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    createTime = db.Column(db.DateTime, default=datetime.utcnow)
    inspireTime = db.Column(db.Time, nullable=False)
    expireTime = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('Users', backref=db.backref('task', lazy=True))

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if password == None :
            error = 'Please enter a password'
            return render_template('signin.html', error=error)
        else:
            new_user = Users(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/sign_in')

    else:
        return render_template('signin.html')


@app.route('/sign_in', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user == None:
            error = 'User not found!'
            return render_template('login.html', error=error)
        if user.password == password :
            return redirect(url_for('dashboard', username=username))
        else:
            error = 'Password is wrong!'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.route('/<username>/dash/', methods=['POST', 'GET'])
def dashboard(username):
    if username == 'admin':
        user = Users.query.filter_by(username=username).first()
        users = Users.query.all()
        return render_template('admins.html', users=users, username=user.username)
    else:
        user = Users.query.filter_by(username=username).first()
        user_tasks = Users.query.get(user.id).task

        return render_template('dash.html', tasks=user_tasks, username=user.username)


@app.route('/<username>/dash/add/task/', methods=['POST', 'GET'])
def addtaskpage(username):
    user = Users.query.filter_by(username=username).first()
    return render_template('newTask.html', username=user.username)


@app.route('/<username>/dash/add/task/done/', methods=['POST', 'GET'])
def addtask(username):
    if request.method == 'POST':
        user = Users.query.filter_by(username=username).first()
        title = request.form['title']
        description = request.form['description']
        inspireTime_str = request.form['inspire']
        expireTime_str = request.form['expire']
        try:
            # Convert the string input to a time object
            inspireTime = datetime.strptime(inspireTime_str, '%H:%M').time()
            expireTime = datetime.strptime(expireTime_str, '%H:%M').time()
        except ValueError:
            # Handle the error if the input does not match the expected format
            # You can set a default time or return an error message
            pass
        new_task = Tasks(user_id=user.id,  title=title, description=description, inspireTime=inspireTime, expireTime=expireTime)
        try:
            db.session.add(new_task)
            db.session.commit()
            print('1')
            return redirect(url_for('dashboard', username=username))
        except:
            return 'issue'
    else:
        print("dddd")
        return render_template('newTask.html')


@app.route('/<username>/task/delete/<int:id>')
def delete_task(username, id):
    task_delete = Tasks.query.get_or_404(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect(url_for('dashboard', username=username))
    except:
        return 'error'


@app.route('/<username>/user/delete/<int:id>')
def delet_user(username, id):
    try:
        user = Users.query.get_or_404(id)
        Tasks.query.filter_by(user_id=id).delete()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('dashboard', username=username))
    except:
        return 'error'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
