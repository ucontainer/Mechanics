from app.extensions import ma
from app.models import Invoice
from marshmallow import fields
from app.blueprints.mechanics.mechSchemas import MechanicSchema
from app.blueprints.user.userSchemas import CustomerSchema

class TicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested(MechanicSchema(exclude=("email","password","phone","salary")),many=True)
    customer = fields.Nested(CustomerSchema)
    class Meta:
        model = Invoice
        include_fk = True
        # fields = ("ticket_id","ticket_date","user_id", "tickets", "ticket_holder","id")
        
class EditTicketSchema(ma.Schema):
    add_ticket_ids = fields.List(fields.Int(), required=True)
    remove_ticket_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_mechanic_ids","remove_mechanic_ids")
    
ticket_schema = TicketSchema()  #used to serialize a single customer object.
tickets_schema = TicketSchema(many=True)  #used to serialize many customer objects

edit_ticket_schema = EditTicketSchema