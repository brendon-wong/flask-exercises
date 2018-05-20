from solution import db, Snack

# Seed the app with snacks
db.create_all()

lays = Snack("Lays", "Chips")
doritos = Snack("Doritos", "Chips")
cheetos = Snack("Cheetos", "Chips")
apples = Snack("Apples", "Fruits")
oranges = Snack("Oranges", "Fruits")
almonds = Snack("Almonds", "Nuts")

db.session.add_all([lays, doritos, cheetos, apples, oranges, almonds])
db.session.commit()