from application import db
from datetime import datetime
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


# A Menu Item
class MenuItem(object):
	def __init__(self, name, text, img, price, options, category):
		self.name = name
		self.text = text
		self.img = img
		self.price = price
		self.options = options
		self.category = category

	def __str__(self):
		return 'MenuItem(name={}, text={}, img={}, price={}, options={}'.format(
			self.name, self.text, self.img, self.price, self.options)

	def __repr__(self):
		return self.__str__()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(255), nullable=False)
	password = db.Column(db.String(255), nullable=False)
	phone = db.Column(db.String(255), nullable=False)
	orders = db.relationship('Order', backref='author', lazy=True)


	def __repr__(self):
		return f"User('{self.name}', '{self.email}', '{self.password}' ,'{self.phone}')"

class Order(db.Model):
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	order_num = db.Column(db.Integer, primary_key=True)
	food_id = db.Column(db.String(255), nullable=False)
	data_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	status = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return f"Order('{self.food_id}','{self.data_posted}', '{self.status}')"

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
