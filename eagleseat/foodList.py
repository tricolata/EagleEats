from app import db, MenuItemDb

db.session.query(MenuItemDb).delete()
db.session.commit()

first = ['Chicken Fingers', 'Description', 'garden-fresh-slate-compressed.jpg', 5.99,'{"options":["Ranch"]}', 'entree', True]
menus = [
['French Fries', 'Description', 'pepperoni-slate-compressed.jpg', 1.99, None,'side', False],
['Ice Cream', 'Description', 'garden-fresh-slate-compressed.jpg', 2.99,'{"options":["Fudge", "Caramel", "Cookie Dough"]}', 'dessert', False],
['Coca Cola', 'Description', 'pepperoni-slate-compressed.jpg', 0.99, None, 'drink', True]
]

# So it can start from 0

m = MenuItemDb(id=0, name=first[0], text=first[1], img=first[2], price=first[3], options=first[4], category=first[5], sized=first[6])
db.session.add(m)

for menu in menus:
	m = MenuItemDb(name=menu[0], text=menu[1], img=menu[2], price=menu[3], options=menu[4], category=menu[5], sized=menu[6])
	db.session.add(m)
db.session.commit()
