""" Flask is a microframework to create web applications within python """

from flask import Flask, render_template, redirect, request, url_for
import sqlite3
from sqlite3 import Error
from classes import MenuItem
from classes import OrderAmount, User, Customer

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
		username = request.form.get("user_id")
		email = request.form.get("email")
		password = request.form.get("password")
		phone = request.form.get("phone")
		address = request.form.get("address")

		with conn:
			customer = (name, username, email, password, phone, address)
			create_user(conn, customer)

		return render_template("index.html")

@app.route("/login")
def login():
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
	menu_items = [
		MenuItem('Chipotle Crispers', 'Crispy coated fried chicken tenders coated in a sweet and spicy honey chipotle sauce.', 'static/img/burger.jpg', 5.99),
		MenuItem('Pizza Pie', 'Pepperoni, clean and simple', 'static/img/burger.jpg', 5.99),
		MenuItem('Angry Pizza Pie', 'Pepperoni Angry Peppers Mushroom Olives Chives', 'static/img/burger.jpg', 5.99)
	]
	orderAmount = OrderAmount()
	for item in menu_items:
		orderAmount.subTotal += item.price
	
	orderAmount.subTotal =(orderAmount.subTotal)
	print(orderAmount.subTotal)
	orderAmount.salesTax = (orderAmount.TAX * orderAmount.subTotal)
	orderAmount.total = (orderAmount.salesTax +  orderAmount.subTotal)
	orderAmount.subTotal = '{:0>2.2f}'.format(orderAmount.subTotal)
	orderAmount.salesTax = '{:0>2.2f}'.format(orderAmount.salesTax)
	orderAmount.total = '{:0>2.2f}'.format(orderAmount.total)
	return render_template("cart.html", menu_items=menu_items, orderAmount=orderAmount)

@app.route("/checkout", methods=["POST", "GET"])
def checkout():
	menu_items = [
		MenuItem('Chipotle Crispers', 'Crispy coated fried chicken tenders coated in a sweet and spicy honey chipotle sauce.', 'static/img/burger.jpg', 5.99),
		MenuItem('Pizza Pie', 'Pepperoni, clean and simple', 'static/img/burger.jpg', 5.99),
		MenuItem('Angry Pizza Pie', 'Pepperoni Angry Peppers Mushroom Olives Chives', 'static/img/burger.jpg', 5.99)
	]
	orderAmount=OrderAmount()
	for item in menu_items:
		orderAmount.subTotal += item.price
	orderAmount.total= '{:.2f}'.format((orderAmount.TAX * orderAmount.subTotal) + orderAmount.subTotal)

	customer = Customer("Jacob Murillo","1234","jacob@mail.com","dsds","000-000-000","riverside tx")
	customer.name = "Jacob Murillo"

	amount = float(orderAmount.total)
	
	if request.method == "POST":
		option = request.form['transaction']
		print(option)
		if option =="creditCard":
			card_number = request.form.get("cardNumber")
			expiration_date = request.form.get("expDate")
	
			print(card_number, expiration_date, amount)
			return redirect(url_for('index'))
		else:
			return redirect(url_for('index'))

	
	return render_template("checkout.html", menu_items=menu_items, orderAmount=orderAmount, customer=customer)