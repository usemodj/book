import unittest, re
from app import create_app, db
from app.models import User, Role
from flask import url_for

class FlaskClientTestCase(unittest.TestCase):
    def setup(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('Stranger' in response.get_data(as_text=True))
        
    def test_register_and_login(self):
        #register an new Account
        response = self.client.post(url_for('auth.register'), data={
                        'email': 'usemodj@gmail.com',
                        'password': '12345',
                        'password2': '12345'
                        })
        self.assertTrue(response.status_code == 302)
        
        #login with the new Account
        response = self.client.post(url_for('auth.login'), data={
                        'email': 'usemodj@gmail.com',
                        'password': '12345'
                        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('Hello,\s+usemodj@gmail.com', data))
        self.assertTrue('You have not confirmed your account yet' in data)
        
        #send a confirmation Token
        user = User.query.filter_by(email='usemodj@gmail.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have confirmed your account' in data)
        
        #log out
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out' in data)
        