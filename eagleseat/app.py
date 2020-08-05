import json

""" Flask is a microframework to create web applications within python """

from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask_mail import Mail, Message

from datetime import timedelta
import os
import os.path
from dotenv import load_dotenv
import random
import threading
import time

# load .env if exists
if os.path.exists('.env'):
	load_dotenv()
else:
	# load .env.example if no .env is present
	print('.env file not found, using example file...')
	load_dotenv(dotenv_path='.env.example')

secret_key = os.getenv('SECRET_KEY')
database_file = os.getenv('DATABASE_FILE')
#database_file = "restaurant.db"
merchant_id = os.getenv('MERCHANT_ID')

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key # import secrets secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_file
db = SQLAlchemy(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_USERNAME'] = 'eagle.eats.2020@gmail.com'
app.config['MAIL_PASSWORD'] = 'Password!!'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

from charge_card import charge
from classes import *
db.create_all()
menu_items = MenuItem.query.order_by(MenuItem.id.asc()).all()

# food processing
def food_manager():
	while True:
		current_order = Order.query.filter_by(status='received').order_by(Order.id.asc()).first()

		if current_order == None:
			# wait 1 minute before trying again
			time.sleep(5)
		else:
			print(f'cooking order {current_order.id}...')

			food_list = json.loads(current_order.food_list)

			# calculate cook time
			total_cook_time = 0
			for item in food_list['items']:
				total_cook_time += menu_items[int(item['id'])].cook_time

			# update status
			current_order.status = 'cooking'
			db.session.commit()

			# "cook" food
			time.sleep(total_cook_time)

			# update status
			current_order.status = 'ready'
			db.session.commit()

			print(f'finished cooking order {current_order.id}!')

food_manager_thread = threading.Thread(target=food_manager)
food_manager_thread.daemon = True # this thread dies when main thread dies
food_manager_thread.start()

# randomly pick 4 deal items
deal_items = []
while len(deal_items) < 5:
	# get random item from menu_items
	deal_item = random.choice(menu_items)

	# add deal_item if it is not already in deal_items
	if deal_item not in deal_items and deal_item.category != 'drink':
		deal_items.append(deal_item)

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

		msg = Message('EagleEats', sender='eagle.eats.2020@gmail.com', recipients=[email])
		msg.body="Thank you for registering with EagleEats"
		msg.html=render_template("reg_email.html")
		mail.send(msg)
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
		flash("Wrong email and/or password. Try again")
		return redirect(url_for('login'))

@app.route("/logout")
def logout():
	session['logged_in'] = False
	session['email'] = None
	return redirect(url_for('index'))

@app.route("/deals")
def deals():
	return render_template("menu.html", menu_items=deal_items, delivery_method=session.get('delivery_method'))

@app.route("/menu", methods=["GET"])
def menu():
	menu_items_filtered = []
	unique_names = []
	for item in menu_items:
		if item.name not in unique_names:
			menu_items_filtered.append(item)
			unique_names.append(item.name)

	return render_template("menu.html", menu_items=menu_items_filtered, delivery_method=session.get('delivery_method'))



@app.route("/checkout", methods=["POST", "GET"])
def checkout():
	cart_items = access_cart()
	order = construct_order()
	if order is not None:
		order_price = '{:.2f}'.format(float(order.total_price() * 1.0825)) # with tax
	else:
		order_price = 0
	user = User.query.filter_by(email=session.get('email')).first()

	if request.method == 'POST':
		if order is not None:
			payment_type = request.form['transaction']
			if payment_type == 'creditCard':
				card_number = request.form.get('cardNumber')
				expiration_date = request.form.get('expDate')

				trans_response = charge(card_number, expiration_date, order_price, merchant_id)

				# if card was charged successfully
				# if trans_response[0]:
				if True:
					# add to current order table
					db.session.add(order)
					db.session.commit()

					empty_cart()

					return 'This will redirect to confirmation soon'
				else:
					flash('Card could not be charged succesfully')
					return redirect(url_for('checkout'))
			else:
				# add to current order table
				db.session.add(order)
				db.session.commit()

				empty_cart()
				return 'This will redirect to confirmation soon'
		else:
			flash('No items in order')
			return redirect(url_for('checkout'))
	else:
		return render_template("checkout.html", cart_item=cart_items, orderAmount=order_price, customer=user)

# constructs and returns an order instance
# based on the cart and current user
def construct_order():
	cart_json = session.get('cart')
	user_email = session.get('email')
	user = User.query.filter_by(email=user_email).first()
	if (cart_json is not None and user is not None):
		cart_items = access_cart()
		delivery_method = json.loads(session['cart'])['delivery_method']

		if len(cart_items) > 0:
			order = Order(
				user_id=user.id,
				food_list=cart_json,
				delivery_method=delivery_method,
			)

			return order

	# if we have not returned yet then at least one of the following is true:
	# 1.) cart_json is None
	# 2.) user for current email is None
	# 3.) cart is empty
	return None

# FIXME TODO XXX: TEMPORARY ROUTES FOR HELPING DEVELOPMENT
@app.route("/cart/json")
def cart_json():
	return session['cart']

@app.route("/cart/empty")
def empty_cart_route():
	empty_cart()
	return redirect(url_for('cart_json'))
# FIXME TODO XXX

def build_option_string(option, value):
	# Use `No` instead of `None` in option string
	# e.g. None Pickles -> No Pickles
	if value == 'None':
		return 'No ' + option
	else:
		return value.capitalize() + ' ' + option.capitalize()

@app.route("/cart", methods=["GET", "POST"])
def cart():
	if session.get('logged_in') != True:
		flash('You must be logged in to place an order')
		return redirect(url_for('login'))
	else:
		# create cart if not already there
		if session.get('cart') is None:
			init_cart()

		if request.method == "POST":
			id = request.form.get('id')
			if session.get('delivery_method') is None:
				delivery_method = request.form.get('deliveryMethod')
				session['delivery_method'] = delivery_method
				set_delivery_method(delivery_method)

			options = []
			for field in request.form:
				# already grabbed ID, so skip it
				if field == 'id':
					continue

				# already grabbed deliveryMethod, so skip it
				if field == 'deliveryMethod':
					continue

				field_value = request.form.get(field)

				# if field is a size, then value is added to ID to get
				# the 'real' ID of the menu item
				if field == 'size':
					# calculate 'real' ID of size item
					if field_value == 'small':
						id = str(int(id) + 0)
					elif field_value == 'medium':
						id = str(int(id) + 1)
					elif field_value == 'large':
						id = str(int(id) + 2)
					elif field_value == 'giant':
						id = str(int(id) + 3)
				else:
					# everything else is an option string
					# NOTE: only add modifications (e.g. not 'Regular')
					if field_value != 'regular':
						options.append(build_option_string(field, field_value))

			add_to_cart(id, options)
			# return to menu
			return redirect(url_for('menu'))
		else:
			orderAmount = OrderAmount()
			cart_item =access_cart()
			user = User.query.filter_by(email=session['email']).first()
			for item in cart_item:
				orderAmount.subTotal += item.price
				
			orderAmount.subTotal =(orderAmount.subTotal)
			orderAmount.salesTax = (orderAmount.TAX * orderAmount.subTotal)
			orderAmount.total = (orderAmount.salesTax +  orderAmount.subTotal)
			orderAmount.subTotal = '{:0>2.2f}'.format(orderAmount.subTotal)
			orderAmount.salesTax = '{:0>2.2f}'.format(orderAmount.salesTax)
			orderAmount.total = '{:0>2.2f}'.format(orderAmount.total)
			return render_template("cart.html", cart_item = cart_item ,orderAmount=orderAmount, user=user)

def init_cart():
	# json boilerplate
	session['cart'] = '{"delivery_method": "","items":[]}'

def set_delivery_method(method):
	cart = json.loads(session['cart'])
	cart['delivery_method'] = method
	session['cart'] = json.dumps(cart)

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

	session.pop('delivery_method', None)

	init_cart()

	return session['cart']

def access_cart():
	cart = json.loads(session['cart'])
	cart_item = []
	for item in cart['items']:
		cart_item.append(menu_items[int(item['id'])])
	return cart_item

@app.route("/aboutus")
def aboutus():
	return render_template("aboutus.html")

@app.route("/account", methods=["GET", "POST"])
def account():
	if session.get('logged_in') is not None:
		if request.method == 'GET':
			if not session['logged_in']:
				return redirect(url_for('index'))
			else:
				user = User.query.filter_by(email=session['email']).first()

				return render_template('account.html', user=user)
		else:
			if not session['logged_in']:
				return redirect(url_for('index'));
			else:
				user = User.query.filter_by(email=session['email']).first()

				if user is not None:
					# update email
					email = request.form.get('email')
					if user.email != email:
						# if email not already in system
						if User.query.filter_by(email=email).first() is not None:
							flash('That email already exists, please try another')
							return redirect(url_for('account'))
						else:
							user.email = email
							session['email'] = email

					# update password
					old_password = request.form.get('old-password');

					# if passwords are present
					if len(old_password) > 0:
						if sha256_crypt.verify(old_password, user.password):
							password = sha256_crypt.encrypt(request.form.get('new-password'))
							user.password = password
						else:
							flash('Incorrect password. Try again')
							return redirect(url_for('account'))

					# update phone and name
					phone = request.form.get('phone')
					name = request.form.get('name')

					user.phone = phone
					user.name = name

					# commit user to db
					db.session.commit()

			return redirect(url_for('index'))
	else:
		return redirect(url_for('index'))

@app.route("/tracker/<order_id>", methods=["GET"])
def tracker(order_id):
	order = Order.query.filter_by(id=order_id).first();

	# handle order not found
	if order is None:
		return render_template('tracker.html', order=None, attempted_id=order_id)

	order_items = json.loads(order.food_list);
	
	items = []
	total_cook_time = 0
	# construct food list
	for item_json in order_items['items']:
		# item dict
		item = {}

		item_name = menu_items[int(item_json['id'])].name

		size = menu_items[int(item_json['id'])].size
		if size is not None:
			item_name = size + ' ' + item_name

		item['name'] = item_name

		mods = []
		for option in item_json['options']:
			mods.append(option)

		item['mods'] = mods

		total_cook_time += menu_items[int(item_json['id'])].cook_time

		items.append(item)

	expected_time = order.date_posted + timedelta(seconds=total_cook_time)

	return render_template('tracker.html', order=order, items=items, expected_time=expected_time.strftime('%I:%M%p'))

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

if __name__ == '__main__':
	app.run()
