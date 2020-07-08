""" Flask is a microframework to create web applications within python """

from flask import Flask, render_template, redirect, request, url_for, flash
from passlib.hash import sha256_crypt
import sqlite3
from sqlite3 import Error
from classes import MenuItem
from classes import User
import random
import os


used_ids = []
""" Create a database connection to SQLite database """
def create_connection(db_name):
	conn = None
	try:
		conn = sqlite3.connect(db_name)
		return conn
	except Error as e:
		print(e)

	return conn
""" Create a new user into the customers table """
def create_user(conn, user):
	sql = ''' INSERT INTO customers(user_id, name, email, password, phone) VALUES (?,?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, user)
	return cur.lastrowid	# lastrowid attributes the cursor object to get back generated id

app = Flask(__name__)
app.secret_key = os.urandom(12)

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
		database = "restaurant.db"
		conn = create_connection(database)

		""" request.form.get() accesses to input from html file """

		name = request.form.get("name")
		email = request.form.get("email")
		password = sha256_crypt.encrypt(request.form.get("password"))
		phone = request.form.get("phone")
		# random() could give same number so this will check
		r = random.randint(1,200000)
		while r in used_ids:
			r = random.randint(1,200000)
		used_ids.append(r)
		user_id = r

		with conn:
			sql = ''' SELECT * FROM customers where email = ? '''
			cur = conn.cursor()
			cur.execute(sql, (email, ))
			if cur.fetchone():
				flash("That email already exist, please log in or choose another")
				return redirect(url_for('register'))
			else:
				customer = (user_id, name, email, password, phone)
				create_user(conn, customer)
				return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		database = "restaurant.db"
		conn = create_connection(database)

		email = request.form.get("email")
		password = request.form.get("password")

		sql = ''' SELECT password FROM customers WHERE email = ? '''
		cur = conn.cursor()
		cur.execute(sql, (email, ))
		if not sha256_crypt.verify(password, cur.fetchone()[0]):
			flash("Wrong email and/or password. Try again")
			return redirect(url_for('login'))
		else:
			return render_template("index.html")
	else:
		return render_template("login.html")
@app.route("/deals")
def deals():
	# TODO: get deals

	return render_template("deals.html")

@app.route("/menu", methods=["GET"])
def menu():
	# TODO: Read items from somwehere
	menu_items = [
		MenuItem('Chipotle Crispers', 'Crispy coated fried chicken tenders coated in a sweet and spicy honey chipotle sauce.', 'static/img/garden-fresh-slate-compressed.jpg', 5.99),
		MenuItem('Pizza Pie', 'Pepperoni, clean and simple', 'static/img/pepperoni-slate-compressed.jpg', 5.99),
		MenuItem('Angry Pizza Pie', 'Pepperoni Angry Peppers Mushroom Olives Chives', 'static/img/garden-fresh-slate-compressed.jpg', 5.99),
		MenuItem('Smol Pizza Pie', 'Pepperoni but smol', 'static/img/pepperoni-slate-compressed.jpg', 5.99),
		MenuItem('Baked Potatoes', 'I like to eat potatoes but not french fries', 'static/img/pepperoni-slate-compressed.jpg', 5.99),
	]

	return render_template("menu.html", menu_items=menu_items)

@app.route("/cart")
def cart():
	# TODO: read cart data
	return render_template("cart.html")
