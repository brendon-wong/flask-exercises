from project import db

from project.users.models import User
from project.messages.models import Message
from project.tags.models import Tag

# Delete existing data, if any
db.drop_all()

# Create tables and database
db.create_all()

# Create users

joe = User("Joe", "Bloggs", "joe", "password")
maria = User("Maria", "Rossi", "maria", "password")
fulan = User("Fulan", "AlFulani", "fulan", "password")
taro = User("Taro", "Yamada", "taro", "password")

# Create messages

weather = Message("The weather is nice today", 1)
life = Message(
    "Do not take life too seriously. You will never get out of it alive.", 1)
brain = Message(
    "Maybe if we tell people the brain is an app, they'll start using it.", 1)
italy = Message("I love Italy!", 2)
arabic = Message("Arabic has 11 words for love, and hundreds for camel.", 3)
dancing = Message("Late-night dancing was illegal in Japan until 2015.", 4)
adoption = Message(
    '98% of adoptions in Japan are of adult men to keep businesses "in the family."', 4)

# Create tags

small_talk = Tag("Small Talk")
country = Tag("Country")
japan = Tag("Japan")
quote = Tag("Quote")

# Create M:N relationships

weather.tags.extend([small_talk])
life.tags.extend([quote])
brain.tags.extend([quote])
italy.tags.extend([country, small_talk])
arabic.tags.extend([country])
dancing.tags.extend([country, japan])
adoption.tags.extend([country, japan])

# Commit changes

db.session.add_all([joe, maria, fulan, taro])
db.session.add_all([weather, life, brain, italy, arabic, dancing, adoption])
db.session.add_all([small_talk, country, japan, quote])
db.session.commit()
