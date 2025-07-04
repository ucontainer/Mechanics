from marshmallow import ValidationError
from flask import request, jsonify
from sqlalchemy import select
from .mechSchemas import mechanic_schema, mechanics_schema
from app.models import Mechanics, db
from . import mechanics_bp




#Route creation:
    #Create customer
    #Use the route to send requests to a specific function

@mechanics_bp.route('/',methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanics).where(Mechanics.email == mechanic_data['email'])
    existing_mechanic = db.session.execute(query).scalars().all()
    if existing_mechanic:
        return jsonify({"error": "Email already exists"}), 404
    new_mechanic = Mechanics(**mechanic_data)   #** unpacks the dictionary
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

    #Get all customers
@mechanics_bp.route('/',methods=['GET'])
def get_mechanics():
    query = select(Mechanics)
    mechanics_all = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics_all)

    #Get specific customer
@mechanics_bp.route('/<int:mechanic_id>',methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic=db.session.get(Mechanics,mechanic_id)   
    
    if mechanic:
        return mechanic_schema.jsonify(mechanic),200
    return jsonify({'error':'Mechanic does not exist.'}),404

    #Update a customer (PUT)
@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics,mechanic_id)
    
    if not mechanic:
        return jsonify({'error','Mechanic does not exist'}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for k, v in mechanic_data.items():
        setattr(mechanic,k,v)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic),200    
    
    #Delete a mechanic(DELETE)
@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic=db.session.get(Mechanics, mechanic_id)
    
    if not mechanic:
        return jsonify({'error','Mechanic does not exist'}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message':f'Mechanic id: {mechanic_id}, successfully deleted'}), 200