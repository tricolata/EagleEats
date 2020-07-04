""" Flask is a microframework to create web applications within python """

from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error
from classes import MenuItem

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
	sql = ''' INSERT INTO customers(name, user_id, email, password, phone, address) VALUES (?,?,?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, user)
	return cur.lastrowid	# lastrowid attributes the cursor object to get back generated id

app = Flask(__name__)

""" route() tells flask what URL triggers this function """
@app.route("/")
def index():
	return render_template("index.html")

""" registration route """
""" GET request loads login/signup page, POST request adds new account to db"""
@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "GET":
		return render_template("signup.html")
	else:
		database = "restaurant.db"
		conn = create_connection(database)

		""" request.form.get() accesses to input from html file """

		name = request.form.get("name")
		username = request.form.get("user_id")
		email = request.form.get("email")
		password = request.form.get("password")
		phone = request.form.get("phone")
		address = request.form.get("address")

		with conn:
			customer = (name, username, email, password, phone, address)
			create_user(conn, customer)

		return render_template("index.html")

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
