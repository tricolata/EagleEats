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
	def __init__(self, name, text, img, price):
		self.name = name
		self.text = text
		self.img = img
		self.price = price

	def __str__(self):
		return 'MenuItem(name={}, text={}, img={}, price={}'.format(
			self.name, self.text, self.img, self.price)

	def __repr__(self):
		return self.__str__()

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
