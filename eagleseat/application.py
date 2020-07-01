""" Flask is a microframework to create web applications within python """

from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

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
