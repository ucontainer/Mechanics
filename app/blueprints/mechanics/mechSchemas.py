from app.extensions import ma
from app.models import Mechanics


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics
mechanic_schema = MechanicSchema()  #used to serialize a single customer object.
mechanics_schema = MechanicSchema(many=True)  #used to serialize many customer objects.
