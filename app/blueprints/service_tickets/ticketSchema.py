from app.extensions import ma
from app.models import Invoice
from marshmallow import fields


class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice
        include_fk = True
        
class EditTicketSchema(ma.Schema):
    add_loan_ids = fields.List(fields.Int(), required=True)
    remove_loan_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_mechanic_ids","remove_mechanic_ids")
    
ticket_schema = TicketSchema()  #used to serialize a single customer object.
tickets_schema = TicketSchema(many=True)  #used to serialize many customer objects

edit_ticket_schema = EditTicketSchema