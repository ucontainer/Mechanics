from marshmallow import ValidationError
from flask import request, jsonify
from sqlalchemy import select
from .ticketSchema import ticket_schema, tickets_schema
from app.blueprints.mechanics.mechSchemas import mechanic_schema, mechanics_schema 
from app.models import Invoice, db
from app.models import Mechanics, db
from . import tickets_bp



#Route creation:
    #Create ticket
    #Use the route to send requests to a specific function
    
@tickets_bp.route('/', methods=['GET'])
def get_tickets():
    query = select(Invoice)
    tickets_all = db.session.execute(query).scalars().all()
    
    return tickets_schema.jsonify(tickets_all)


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

@tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>',methods=(['PUT']))
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Invoice, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if ticket and mechanic:
        if mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)
            db.session.commit()
            return jsonify({
                "message":"successfully added mechanic to ticket",
                "ticket": ticket_schema.dump(ticket),
                "mechanic": mechanic_schema.dump(ticket.mechanics)
            }), 200
       
        return jsonify({'error':'Mechanic does not exist'}), 404
    return jsonify({"error":"Invalid ticket_id or mechanic_id"}), 404

@tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Invoice, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if ticket and mechanic:
        if mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
            db.session.commit()
            return jsonify({
                "message":"successfully removed mechanic from ticket",
                "ticket": ticket_schema.jsonify(ticket),
                "mechanics": mechanics_schema.jsonify(ticket.mechanics)
                }), 200
        return jsonify({'error':'Mechanic does not exist'}), 404
    return jsonify({"error":"Invalid ticket_id or mechanic_id"}), 404
    
    