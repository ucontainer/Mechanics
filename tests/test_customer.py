from app import create_app
from app.models import db, Customer
from app.utils.util import encode_token
import unittest

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customer(name='test_user',email='test@email.com',address='123 test way, Nami OJ 11000',password='321')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()
        
    def test_create_customer(self):
        customer_payload = {
            "name":"joel doe",
            "email": "stringify@string.str",
            "address": "123 string way, NY, NY 10001",
            "password": "string"
        }
        response = self.client.post('/customers/',json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "joel doe")
        
    def test_invalid_creation(self):
        customer_payload = {
            "name":"joel doe",
            "address": "123 string way, NY, NY 10001",
            "password": "string"
        }
        response = self.client.post('/customers/',json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field'])
        
    def test_login_customer(self):
        credentials = {
            'email' : 'test@email.com',
            'password' : '321'
        }
        response = self.client.post('/customers/login',json=credentials)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']
    
    def test_invalid_login(self):
        credentials = {
            "email" : "nahim@failtest.com",
            "password" : "909"
        }
        response = self.client.post('/customers/login',json=credentials)
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json['message'], 'Invalid email or password!')
    
    def test_update_customer(self):
        update_payload = {
            "name" : "peter",
            "email" : "",
            "address" : "",
            "password" : ""
        }   
        headers ={'Authorization' : "Bearer "+self.test_login_customer()}
        response = self.client.put('/customers/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'peter')
        self.assertEqual(response.json['email'], 'nahim@failtest.com') 