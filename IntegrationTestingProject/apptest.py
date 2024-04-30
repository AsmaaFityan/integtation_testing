import os
import unittest
import sqlite3
import tempfile
import uuid
from app import app, get_db_connection

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # Configure the app for testing
        app.config['TESTING'] = True

        # Setup an in-memory SQLite database for testing
        app.config['DATABASE'] = 'sqlite:///:memory:'

        # Initialize the in-memory database
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.test_client()

        with app.app_context():
            conn = get_db_connection()
            conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)')
            conn.commit()
        print('setUp Testcase Done')
    
    def test_register_post(self):
        unique_username = f"testuser_{uuid.uuid4()}"
        response = self.app.post('/register', data={'username': unique_username, 'password': 'testpass'}, follow_redirects=True)
        
        # Debug output
        print(response.data.decode())
        
        # Check if the user is redirected to the success page
        self.assertEqual(response.status_code, 200, "Expected a successful response after registration")
        self.assertIn('User created successfully', response.data.decode(), "The success message isn't in the response")

        # Check the database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (unique_username,))
        user = cur.fetchone()
        self.assertIsNotNone(user, "User was not added to the database")
        self.assertEqual(user['username'], unique_username)
        print('test_register_post Testcase Done')
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
        print('tearDown Testcase Done')
# if _name_ == '_main_':
#     unittest.main()