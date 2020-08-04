from app import db
from classes import MenuItem

db.session.query(MenuItem).delete()
db.session.commit()

# list of menu items. schema:
# [name, description, img url, price, options json, category, sized]
menu_items = [
	['Chicken Fingers', 'Description', 'garden-fresh-slate-compressed.jpg', 6.99,'{"options":["Ranch"]}', 'entree', 3, False],
	['French Fries', 'Description', 'pepperoni-slate-compressed.jpg', 1.99, None,'side', 3, True],
	['Ice Cream', 'Description', 'garden-fresh-slate-compressed.jpg', 2.99,'{"options":["Fudge", "Caramel", "Cookie Dough"]}', 'dessert', 3, True],
	['Coca Cola', 'Description', 'pepperoni-slate-compressed.jpg', 0.99, None, 'drink', 3, True]
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
