from app import db
from datetime import datetime
import json
# Review, Order, and User definitions


# A review submitted by a Customer
class Review(object):
	def __init__(self, text, date, user_id):
		self.text = text
		self.date = date
		self.user_id = user_id

	def __str__(self):
		return 'Post(text={}, date={}, user_id={})'.format(
			self.text, self.date, self.user_id)

	def __repr__(self):
		return self.__str__()

class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	food_list = db.Column(db.String(512), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	delivery_method = db.Column(db.String(8), nullable=False)
	status = db.Column(db.String(20), nullable=False, default='received')

	def total_price(self):
		sum = 0
		food_items = json.loads(self.food_list)['items']
		for item in food_items:
			menu_item = MenuItem.query.filter_by(id=item['id']).first()
			sum += menu_item.price

		return sum

	def __repr__(self):
		return f"Order('{self.user_id}','{self.food_id}','{self.data_posted}', '{self.status}')"

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(255), nullable=False)
	password = db.Column(db.String(255), nullable=False)
	phone = db.Column(db.String(255), nullable=False)
	orders = db.relationship('Order', backref='author', lazy=True)


	def __repr__(self):
		return f"User('{self.name}', '{self.email}', '{self.password}' ,'{self.phone}')"

class MenuItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	text = db.Column(db.String(255), nullable=False)
	img = db.Column(db.String(255), nullable=False)
	price = db.Column(db.Integer, nullable=False)
	options = db.Column(db.String(255), nullable=True)
	category = db.Column(db.String(255), nullable=False)
	size = db.Column(db.String(8), nullable=True)

	def __repr__(self):
		return f"MenuItemDb('{self.name}','{self.text}', '{self.img}', '{self.price}')"


class Customer(User):
	def __init__(self, name, user_id, email, password, phone, address):
		super().__init__(name, user_id, email, password)
		self.phone = phone
		self.address = address

	def __str__(self):
		return 'Customer(name={}, user_id={}, email={}, password={}, phone={}, address={})'.format(
			self.name, self.user_id, self.email, self.password, self.phone,
			self.address)

	def __repr__(self):
		return self.__str__()


class Employee(User):
	def __init__(self, name, user_id, email, password, position):
		super().__init__(name, user_id, email, password)
		self.position = position

	def __str__(self):
		return 'Employee(name={}, user_id={}, email={}, password={}, position={})'.format(
			self.name, self.user_id, self.email, self.password, self.position)

	def __repr__(self):
		return self.__str__()

#this will take care of the orderAmount fields in the cart
class OrderAmount(object):
	def __init__(self):
		self.subTotal = 0.0
		self.TAX = .0825
		self.salesTax=0.0
		self.total = 0.0
		

	def __str__(self):
		return 'OrderAmount(subTotal={}, TAX={}, total{})'.format(
			self.subTotal, self.TAX, self.total)

	def __repr__(self):
		return self.__str__()

'''

# A food order
class Order(object):
	def __init__(self, order_id, date, status, customer_id, employee_id):
		self.order_id = order_id
		self.date = date
		self.status = status
		self.customer_id = customer_id
		self.employee_id = employee_id

	def __str__(self):
		return 'Order(order_id={}, date={}, status={}, customer_id={}, employee_id={}'.format(
			self.order_id, self.date, self.status, self.customer_id,
			self.employee_id)

	def __repr__(self):
		return self.__str__()


# A generic site user
class User(object):
	def __init__(self, name, user_id, email, password):
		self.name = name
		self.user_id = user_id

		# email pulls double duty as email and username
		self.email = email

		# hashed and salted password
		self.password = password

	def __str__(self):
		return 'User(name={}, user_id={}, email={}, password={})'.format(
			self.name, self.user_id, self.email, self.password)

	def __repr__(self):
		return self.__str__()

'''
