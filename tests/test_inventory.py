from app import create_app
from app.models import db, Inventory
from datetime import datetime
import unittest
from tests.test_customer import TestCustomer

class TestInventory(unittest.TestCase):
    def setup(self):
        self.app = create_app("TestingConfig")
        self.inventory = Inventory(inventory_name="test_inventory",price=29.99)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.inventory)
            db.session.commit()
        self.client = self.app.test_client()
    
    def test_create_inventory(self):
        inventory_payload = {
            "inventory_name":"water bottle",
            "price":"9.99"
        }
        response = self.client.post('/inventory/',json=inventory_payload)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json['inventory_name'],'water bottle')
        
    def test_invalid_creation(self):
        inventory_payload = {
            "inventory_name":"book"
        }
        response = self.client.post("/inventory/",json=inventory_payload)
        self.assertEqual(response.status_code,404)
        self.assertEqual(response.json["inventory_name"],"book")
    
    def test_update_inventory(self):
        update_payload = {
            "inventory_name":"biology book",
            "price":"24.99"
        }
        headers = {"Authorization":"Bearer "+self.test_login_customer()}
        