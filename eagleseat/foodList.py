from app import db
from classes import MenuItem

db.session.query(MenuItem).delete()
db.session.commit()

# list of menu items. schema:
# [name, description, img url, price, options json, category, cook_time, sized]
menu_items = [
	['Chicken Fingers', 'Description', 'chickenStrips.jpg', 6.99,'{"options":["Ranch"]}', 'entree', 3, False],
	['French Fries', 'Description', 'frenchFries.jpg', 1.99, None,'side', 3, True],
	['Ice Cream', 'Description', 'iceCream.jpg', 2.99,'{"options":["Fudge", "Caramel", "Cookie Dough"]}', 'dessert', 3, True],
	['Coca Cola', 'Description', 'coke.jpg', 0.99, None, 'drink', 3, True],
	['Steak Fingers', 'Description', 'steakFingers.jpg', 6.99,'{"options":["Ranch"]}', 'entree', 3, False],
	['Mean Green Burger', 'Description', 'burger.jpg', 8.99, None, 'entree', 3, False],
	['Hot Dog', 'Description', 'hotDog.jpg', 3.99,'{"options":["Mustard, Ketchup, Mayo"]}', 'entree', 3, False],
	['BLT', 'Description', 'BLT.jpg', 4.99,'{"options":["Honey Mustard"]}', 'entree', 3, False],
	['Sloppy Joe', 'Description', 'sloppyJoe.jpg', 6.99,None, 'entree', 3, False],
	['Pancakes', 'Description', 'pancakes.jpg', 6.99,'{"options":["syrup"]}', 'entree', 3, False],
	['French Toast', 'Description', 'frenchToast.jpg', 6.99,'{"options":["syrup"]}', 'entree', 3, False],
	['Chicken and Waffles', 'Description', 'waffles.jpg', 8.99,'{"options":["Honey"]}', 'entree', 3, False],
	['Shrimp Tacos', 'Description', 'shrimpTaco.jpg', 7.99,'{"options":["Salsa Verde"]}', 'entree', 3, False],
	['Cinnamon Bun', 'Description', 'cinnamonBun.jpeg', 3.99, None, 'dessert', 3, False],
	['Cheesecake', 'Description', 'cheesecake.jpg', 3.99,'{"options":["Strawberries", "Raspberries", "Chocolate"]}', 'dessert', 3, False],
	['Onion Rings', 'Description', 'onions.jpg', 2.99,'{"options":["Ranch", "Honey Mustard", "Ketchup"]}', 'side', 3, False],
	['Chips and Salsa', 'Description', 'chips.jpg', 3.99, None, 'side', 3, False],
	['Chips and Queso', 'Description', 'queso.jpg', 3.99, None, 'side', 3, False],
	['Hot Wings', 'Description', 'hotwings.jpg', 6.99, None, 'side', 3, False],
	['Red Velvet Cake', 'Description', 'redVelvet.jpg', 3.99, None, 'dessert', 3, False],

]

# start from 0
# this way, it also acts as the index into
# the global menu_item array
id = 0
for info in menu_items:
	# if item is sized
	if info[-1]:
		for size in ['Small', 'Medium', 'Large', 'Giant']:
			item = MenuItem(
				id = id,
				name = info[0],
				text = info[1],
				img = info[2],
				price = info[3],
				options = info[4],
				category = info[5],
				cook_time = info[6],
				size = size
			)

			db.session.add(item)
			id += 1
	else:
		item = MenuItem(
			id = id,
			name = info[0],
			text = info[1],
			img = info[2],
			price = info[3],
			options = info[4],
			category = info[5],
			cook_time = info[6],
			size = None
		)

		db.session.add(item)
		id += 1

db.session.commit()
