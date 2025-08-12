from app import create_app
from app.models import db, Mechanics
from app.utils.util import encode_token
import unittest

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.mechanic = Mechanics(name="test_mech",email='test_email@mail.com',phone='21232312',salary='98',password='123')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()
        
    def test_create_mechanic(self):
        mechanic_payload = {
            "name":"test_mech",
            "email":"test_email@mail.com",
            "phone":"21232312",
            "salary":"98",
            "password":"123"
        }    
        response = self.client.post('/mechanics/',json=mechanic_payload)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json['name'],"test_mech")
        
    def test_invalid_creation(self):
        mechanic_payload = {
            "address":"555 main streat",
            "password":"432"
        }   
        response = self.client.post('/mechanics/',json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['name'], ['Missing data for required field.']) 
        
    def test_login_mechanic(self):
        credentials = {
            "email": "daly.r@yyy.com",
            "password":"45"
        }
        response = self.client.post('/mechanics/login',json=credentials)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']
    
    def test_invalid_login(self):
        credentials = {
            "email": "daly.r@yyy.com",
            "password":"60"
        }
        response = self.client.post('/mechanics/login',json=credentials)
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json['message'], 'Invalid email or password!')
    
    def test_update_mechanic(self):
        update_payload = {
            "name" : "peter",
            "email" : "",
            "phone" : "",
            "salary": "",
            "password" : ""
        }   
        headers ={'Authorization' : "Bearer "+self.test_login_mechanic()}
        response = self.client.put('/mechanics/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'peter')
        self.assertEqual(response.json['email'], 'daly.r@yyy.com') 