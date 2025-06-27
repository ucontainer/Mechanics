from app.extensions import ma
from app.models import Invoice


class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice
        include_fk = True
ticket_schema = TicketSchema()  #used to serialize a single customer object.
tickets_schema = TicketSchema(many=True)  #used to serialize many customer objects