from app.extensions import ma
from app.models import Mechanics
from marshmallow import Schema, fields


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics
class MechanicLoginSchema(Schema):
        email = fields.Email(required=True, error_messages={"required": "Missing data for required field"})
        password = fields.String(required=True, error_messages={"required": "Missing data for required field"})
mechanic_schema = MechanicSchema()  #used to serialize a single customer object.
mechanics_schema = MechanicSchema(many=True)  #used to serialize many customer objects.
login_schema = MechanicLoginSchema() #exludes those as it'll only look for email/pw