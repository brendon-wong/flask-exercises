from solution import db, User, Message

# Create tables and database
db.create_all()

# Create users

joe = User("Joe", "Bloggs")
maria = User("Maria", "Rossi")
fulan = User("Fulan", "AlFulani")
taro = User("Taro", "Yamada")

# Create messages

weather = Message("The weather is nice today", 1)
life = Message(
    "Do not take life too seriously. You will never get out of it alive.", 1)
brain = Message(
    "Maybe if we tell people the brain is an app, they'll start using it.", 1)
italy = Message("I love Italy!", 2)
arabic = Message("Arabic has 11 words for love, and hundreds for camel.", 3)
japan = Message("Late-night dancing was illegal in Japan until 2015.", 4)

db.session.add_all([joe, maria, fulan, taro])
db.session.add_all([weather, life, brain, italy, arabic, japan])
db.session.commit()
