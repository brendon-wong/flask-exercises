from solution import app, db, User, Message
from flask_testing import TestCase
import unittest


class BaseTestCase(TestCase):
    # Required by Flask-Testing, must return a Flask instance
    def create_app(self):
        # SQLite3 is faster to test with than Postgres
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
        return app

    # setUp and tearDown will be executed before and after each test method
    def setUp(self):
        db.create_all()
        joe = User("Joe", "Bloggs")
        maria = User("Maria", "Rossi")
        fulan = User("Fulan", "AlFulani")
        taro = User("Taro", "Yamada")
        db.session.add_all([joe, maria, fulan, taro])
        weather = Message("The weather is nice today", 1)
        life = Message(
            "Do not take life too seriously. You will never get out of it alive.", 1)
        brain = Message(
            "Maybe if we tell people the brain is an app, they'll start using it.", 1)
        italy = Message("I love Italy!", 2)
        arabic = Message(
            "Arabic has 11 words for love, and hundreds for camel.", 3)
        dancing = Message(
            "Late-night dancing was illegal in Japan until 2015.", 4)
        adoption = Message(
            '98% of adoptions in Japan are of adult men to keep businesses "in the family."', 4)
        db.session.add_all(
            [weather, life, brain, italy, arabic, dancing, adoption])
        db.session.commit()

    def tearDown(self):
        # Ensure SQLAlchemy session is properly removed and new session started with each test
        db.session.remove()
        db.drop_all()

    # Test CRUD on Users

    def test_users_read(self):
        response = self.client.get(
            '/users'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Joe Bloggs', response.data)
        self.assertIn(b'Maria Rossi', response.data)
        self.assertIn(b'Fulan AlFulani', response.data)
        self.assertIn(b'Taro Yamada', response.data)

    def test_users_new_page(self):
        response = self.client.get(
            '/users/new'
        )
        self.assertEqual(response.status_code, 200)

    def test_users_create(self):
        response = self.client.post(
            '/users',
            data=dict(first_name="New", last_name="User"),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New User', response.data)

    def test_users_edit_page(self):
        response = self.client.get(
            '/users/4/edit'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Taro', response.data)

    def test_users_update(self):
        response = self.client.patch(
            '/users/4?_method=PATCH',
            data=dict(first_name="Updated", last_name="Name"),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Name', response.data)
        self.assertNotIn(b'Taro', response.data)

    def test_users_delete(self):
        response = self.client.delete(
            '/users/4?_method=DELETE',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Taro', response.data)

    # Test CRUD on Messages

    def test_messages_read(self):
        response = self.client.get(
            '/users/1/messages'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The weather is nice today', response.data)
        self.assertIn(b'You will never get out of it alive.', response.data)
        self.assertIn(b'the brain is an app', response.data)

    def test_messages_new_page(self):
        response = self.client.get(
            '/users/1/messages/new'
        )
        self.assertEqual(response.status_code, 200)

    def test_messages_create(self):
        response = self.client.post(
            '/users/1/messages',
            data=dict(content="New Message"),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Message', response.data)

    def test_messages_edit_page(self):
        response = self.client.get(
            '/users/1/messages/1/edit'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The weather is nice today', response.data)

    def test_messages_update(self):
        response = self.client.patch(
            '/users/1/messages/1?_method=PATCH',
            data=dict(content="Updated Message"),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Message', response.data)
        self.assertNotIn(b'weather', response.data)

    def test_messages_delete(self):
        response = self.client.delete(
            '/users/1/messages/1?_method=DELETE',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'weather', response.data)


# Run tests with python3 solution_test.py
if __name__ == '__main__':
    # Unittest will discover all test methods
    unittest.main()
