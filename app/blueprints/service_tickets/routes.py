from marshmallow import ValidationError
from flask import request, jsonify
from sqlalchemy import select
from .ticketSchema import ticket_schema, tickets_schema
from app.models import Invoice, db
from . import tickets_bp



#Route creation:
    #Create ticket
    #Use the route to send requests to a specific function
@tickets_bp.route('/',methods=['POST'])
def create_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Invoice).where(Invoice.id == ticket_data['id'])
    existing_ticket = db.session.execute(query).scalars().all()
    if existing_ticket:
        return jsonify({"error": "ID already exists"}), 404
    new_ticket = Invoice(**ticket_data)   #** unpacks the dictionary
    db.session.add(new_ticket)
    db.session.commit()
    return ticket_schema.jsonify(new_ticket), 201