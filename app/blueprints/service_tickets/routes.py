from marshmallow import ValidationError
from flask import request, jsonify
from sqlalchemy import select
from .ticketSchema import ticket_schema, tickets_schema, edit_ticket_schema
from app.blueprints.mechanics.mechSchemas import mechanic_schema, mechanics_schema 
from app.blueprints.user.userSchemas import customer_schema
from app.models import Invoice, db
from app.models import Mechanics, db
from app.models import Customer, db
from . import tickets_bp



#Route creation:
    #Create ticket
    #Use the route to send requests to a specific function
    
@tickets_bp.route('/', methods=['GET'])
def get_tickets():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Invoice)
        tickets_all = db.paginate(query,page=page,per_page=per_page)
        return tickets_schema.jsonify(tickets_all), 200
    except:
        query = select(Invoice)
        tickets_all = db.session.execute(query).scalars().all()
        return tickets_schema.jsonify(tickets_all), 200

@tickets_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer_ticket(customer_id):
    customer = db.session.get(Customer, customer_id)
    query = select(Invoice).where(Invoice.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()
    
    if customer:
        return tickets_schema.jsonify(tickets)
    return jsonify({'message':'Invalid customer id.'}), 404


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
            # breakpoint()
            return jsonify({
                "message":"successfully added mechanic to ticket",
                "ticket": ticket_schema.dump(ticket),
                "mechanic": mechanic_schema.dump(ticket.mechanics[0])
            }), 200
       
        return jsonify({'error':'Mechanic does not exist'}), 404
    return jsonify({"error":"Invalid ticket_id or mechanic_id"}), 404

@tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['DELETE'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Invoice, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if ticket and mechanic:
        if mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
            db.session.commit()
            # breakpoint()
            return jsonify({
                "message":"successfully removed mechanic from ticket",
                "ticket": ticket_schema.dump(ticket),
                "mechanics": mechanics_schema.dump(ticket.mechanics)
                }), 200
        return jsonify({'error':'Mechanic does not exist'}), 404
    return jsonify({"error":"Invalid ticket_id or mechanic_id"}), 404

@tickets_bp.route("/<int:ticket_id>", methods=['PUT'])
def edit_ticket(ticket_id):
    #validate data
    try:
        ticket_edits = edit_ticket_schema.load(request.json)
        print("***Ticket:***"+ticket_edits)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Invoice).where(Invoice.id==ticket_id)
    ticket = db.session.execute(query).scalars().first()
    
    for mechanic_id in ticket_edits('add_mechanic_ids'):
        query = select(Mechanics).where(Mechanics.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().all()
        
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic) 
    
    for mechanic_id in ticket_edits('remove_mechanic_ids'):
        query = select(Mechanics).where(Mechanics.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().all()
        
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)    
            
    db.session.commit()
    return ticket_schema.jsonify('Success!\n'+ticket)
    