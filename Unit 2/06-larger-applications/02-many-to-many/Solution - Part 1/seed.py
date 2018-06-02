from app import db, Employee, Department

# Delete existing data, if any
db.drop_all()

# Create tables and database
db.create_all()

# Create employees

joe = Employee("Joe", 2)
maria = Employee("Maria", 11)
fulan = Employee("Fulan", 5)
taro = Employee("Taro", 34)

# Create departments

marketing = Department("Marketing")
hr = Department("Human Resources")
finance = Department("Finance")
production = Department("Production")

# Create relationships

joe.departments.extend([marketing])
maria.departments.extend([marketing])
fulan.departments.extend([finance, hr])
taro.departments.extend([marketing, hr, finance, production])

# Add and commit changes
db.session.add_all([joe, maria, fulan, taro])
db.session.add_all([marketing, hr, finance, production])
db.session.commit()
