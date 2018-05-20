from solution import db, User

# Create tables and database
db.create_all()

# Create users

"""
lays = Snack("Lays", "Chips")
doritos = Snack("Doritos", "Chips")
cheetos = Snack("Cheetos", "Chips")
apples = Snack("Apples", "Fruits")
oranges = Snack("Oranges", "Fruits")
almonds = Snack("Almonds", "Nuts")

db.session.add_all([lays, doritos, cheetos, apples, oranges, almonds])
db.session.commit()"""