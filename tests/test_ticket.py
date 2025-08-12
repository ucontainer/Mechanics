from app import create_app
from app.models import db, Invoice
from app.utils.util import encode_token
from datetime import datetime
import unittest

class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.tickets = Invoice(customer_id=4,ticket_date="2023-07-22")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.tickets)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()
        
    def test_create_ticket(self):
        ticket_payload = {
            "customer_id":4,
            "ticket_date":"2023=07-22"
        }
        response=self.client.post('/tickets/',json=ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['customer_id','4'])
        
    def test_invalid_creation(self):
        ticket_payload = {
            "ticket_date":"2024-02-17"
        }
        response = self.client.post('/tickets/',json=ticket_payload)
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json['customer_id',['Missing data for required field.']])
        