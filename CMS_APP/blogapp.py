from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '074bb1264ef1b7dfb02fb411300884a4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #using sqllite database available in-built in python
db = SQLAlchemy(app)

#User model
class User(db.Model): #inheriting the model from the model available in flask sqlalchemy
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

#Blog post model
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"

#default route or homepage where it would return the list of posts which got posted
@app.route('/')
@app.route('/posts')
def posts():
	posts = Post.query.all()
	posts_dict = {}
	for post in posts:
		posts_dict[post.id] = {'author': post.user_id, 'title': post.title, 'content': post.content, 'date_posted': post.date_posted}
	return jsonify(posts_dict)

#route to create a post
@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
	data = request.get_json()
	if request.method == 'POST':
		title = data['title']
		content = data['content']
		user_id = data['user_id']
		post = Post(title=title, content=content, user_id=user_id)
		db.session.add(post)
		db.session.commit()
	return jsonify({'status':201, 'message':'Post created successfully'})

#route to update a post
@app.route('/post/update', methods=['GET', 'PUT'])
def update_post():
	data = request.get_json()
	if request.method == 'PUT':
		post = Post.qeury.filter(id=data['id']).one()
		if post.title is not None:
			post.title = data['title']
			post.content = data['content']
			db.session.add(post)
			db.session.commit()
			return jsonify({'status':200, 'message': 'Post updated successfully'})
	return jsonify({'status':404, 'message': 'Post not found'})

#route to create the user
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
	data = request.get_json()
	if request.method == 'POST':
		username = data['username']
		email = data['email']
		password = data['password']
		user = User(username=username, email=email, password=password)
		db.session.add(user)
		db.session.commit()
	return jsonify({'status':201, 'message':'User created successfully'})

#route to update an user
@app.route('/user/update', methods=['GET','PUT'])
def update_user():
	data = request.get_json()
	if request.method == 'PUT':
		user = User.qeury.filter(username=data[username]).one()
		if user.username is not None:
			user.email = data['email']
			user.password = data['password']
			db.session.add(user)
			db.session.commit()
			return jsonify({'status':200, 'message': 'User updated successfully'})
	return jsonify({'status':404, 'message': 'User not found'})



if __name__ == '__main__':
	db.create_all() #for creating all the tables
	app.run(debug=True) #running in debug mode for dev purpose