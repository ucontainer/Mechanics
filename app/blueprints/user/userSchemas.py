from app.extensions import ma
from app.models import Customer
from marshmallow import Schema, fields

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
class CustomerLoginSchema(Schema):
        email = fields.Email(required=True, error_messages={"required": "Missing data for required field"})
        password = fields.String(required=True, error_messages={"required": "Missing data for required field"})
customer_schema = CustomerSchema()  #used to serialize a single customer object.
customers_schema = CustomerSchema(many=True)  #used to serialize many customer objects
login_schema = CustomerLoginSchema() #exludes those as it'll only look for email/pw


