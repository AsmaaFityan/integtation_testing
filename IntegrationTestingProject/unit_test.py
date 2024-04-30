import unittest
from flask import Flask, url_for, request, redirect
import os

app = Flask(__name__)

# Sample data to simulate existing users
existing_users = {'existing_user': True}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if username in existing_users:
            return redirect(url_for('register'))
        else:
            existing_users[username] = True
            return redirect(url_for('success'))
    return "Register Page"

@app.route('/success')
def success():
    return "Success Page"

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.context = app.app_context()
        self.context.push()
        # Configure Flask with SERVER_NAME for URL generation
        self.app.config['SERVER_NAME'] = 'localhost'
        # Optionally, configure APPLICATION_ROOT and PREFERRED_URL_SCHEME
        self.app.config['APPLICATION_ROOT'] = '/'
        self.app.config['PREFERRED_URL_SCHEME'] = 'http'

    def tearDown(self):
        self.context.pop()

    def assertRedirects(self, response, expected_url):
        self.assertEqual(response.status_code, 302) # Assuming a redirect status code
        self.assertEqual(response.location, expected_url)

    def test_register_existing_username(self):
        response = self.app.post('/register', data={'username': 'existing_user'})
        self.assertRedirects(response, url_for('register', _external=True))

    def test_register_post(self):
        response = self.app.post('/register', data={'username': 'new_user'})
        self.assertRedirects(response, url_for('success', _external=True))

if __name__ == '__main__':
    unittest.main()
