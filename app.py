# Usage: python app.py

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request, render_template
from flask import redirect, url_for


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)

	def __init__(self, username, email):
		self.username = username
		self.email = email

	def __repr__(self):
		return '<User %r>' % self.username

@app.route('/list/')
def show_users():
	users = User.query.all()
	return render_template('list.tpl.html', users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		#uncatched error unique value in db
		user = User(request.form['username'], request.form['email'])
		db.session.add(user)
		db.session.commit()
		return render_template('register.tpl.html')
	else:
		# save username/password
		return render_template('register.tpl.html')

@app.route('/')
def index():
	#create tables
	db.create_all()
	return redirect(url_for('register'))

app.debug = True
app.run(host='0.0.0.0', port=5001)
