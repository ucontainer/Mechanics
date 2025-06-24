from app.extensions import ma
from app.models import Customer


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
customer_schema = CustomerSchema()  #used to serialize a single customer object.
customers_schema = CustomerSchema(many=True)  #used to serialize many customer objects