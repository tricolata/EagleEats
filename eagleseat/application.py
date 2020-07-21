import json

""" Flask is a microframework to create web applications within python """

from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c3bc4f31ea3e2837690951d1ae7e8c63'	# import secrets secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
db = SQLAlchemy(app)

from classes import MenuItem, User, Order

""" route() tells flask what URL triggers this function """
@app.route("/")
def index():
	return redirect(url_for("deals"))

""" registration route """
""" GET request loads login/signup page, POST request adds new account to db"""
@app.route("/signup", methods=["GET", "POST"])
def register():
	if request.method == "GET":
		return render_template("signup.html")
	else:
		name = request.form.get("name")
		email = request.form.get("email")
		user = User.query.filter_by(email=email).first()
		if user:
			flash("That email is exist. Please choose another")
			return redirect(url_for('register'))
		password = sha256_crypt.encrypt(request.form.get("password"))
		phone = request.form.get("phone")

		user = User(name=name, email=email, password=password, phone=phone)
		db.session.add(user)
		db.session.commit()
		return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	else:
		email = request.form.get("email")
		password = request.form.get("password")

		user = User.query.filter_by(email=email).first()

		if user is not None:
			if sha256_crypt.verify(password, user.password):
				session['logged_in'] = True
				session['email'] = email
				init_cart()
				return redirect(url_for('index'))
		else:
			flash("Wrong email and/or password. Try again")
			return redirect(url_for('login'))

@app.route("/logout")
def logout():
	session['logged_in'] = False
	return redirect(url_for('index'))

@app.route("/deals")
def deals():
	# TODO: get deals

	return render_template("deals.html")

@app.route("/menu", methods=["GET"])
def menu():
	# TODO: Read items from somwehere
	menu_items = [
		MenuItem(0, 'Chicken Fingers', 'Description', 'garden-fresh-slate-compressed.jpg', 5.99, '{"options":["Ranch"]}', 'entree', 'false'),
		MenuItem(1, 'French Fries', 'Description', 'pepperoni-slate-compressed.jpg', 1.99, None, 'side', 'true'),
		MenuItem(2, 'Ice Cream', 'Description', 'garden-fresh-slate-compressed.jpg', 2.99, '{"options":["Fudge", "Caramel", "Cookie Dough"]}', 'dessert', 'true'),
		MenuItem(3, 'Coca Cola', 'Description', 'pepperoni-slate-compressed.jpg', 0.99, None, 'drink', 'true'),
	]
	return render_template("menu.html", menu_items=menu_items)

# FIXME TODO XXX: TEMPORARY ROUTES FOR HELPING DEVELOPMENT
@app.route("/cart/json")
def cart_json():
	return session['cart']

@app.route("/cart/empty")
def empty_cart_route():
	empty_cart()
	return redirect(url_for('cart_json'))
# FIXME TODO XXX

@app.route("/cart", methods=["GET", "POST"])
def cart():
	if request.method == "POST":
		id = request.form.get('id')

		options = []
		for field in request.form:
			# already grabbed ID, so skip it
			if field == 'id':
				continue

			# everything else is an option string
			field_value = request.form.get(field)
			if field_value == 'None':
				option = 'No ' + field
			else:
				option = field_value + ' ' + field

			options.append(option)

		add_to_cart(id, options)

		# return to menu
		return redirect(url_for('menu'))
	else:
		# TODO: read cart data
		return render_template("cart.html")

def init_cart():
	# json boilerplate
	session['cart'] = '{"items":[]}'

def add_to_cart(id, options):
	item = {
		"id": id,
		"options": options
	}

	cart = json.loads(session['cart'])

	cart['items'].append(item)

	session['cart'] = json.dumps(cart)

def remove_from_cart(pos):
	if 0 < pos < len(cart['items']):
		cart = json.loads(session['cart'])

		del cart['items'][pos]

		session['cart'] = json.dumps(cart)

def empty_cart():
	cart = json.loads(session['cart'])

	while len(cart['items']) > 0:
		del cart['items'][0]

	session['cart'] = json.dumps(cart)

	return session['cart']

@app.route("/aboutus")
def aboutus():
	return render_template("aboutus.html")

if __name__ == '__main__':
	app.run()
