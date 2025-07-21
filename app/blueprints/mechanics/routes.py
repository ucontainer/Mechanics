from marshmallow import ValidationError
from flask import request, jsonify
from sqlalchemy import select
from .mechSchemas import mechanic_schema, mechanics_schema, login_schema
from app.models import Mechanics, db
from . import mechanics_bp
from app.extensions import limiter, cache
from app.utils.util import token_required, encode_token



#Route creation:
    #Create customer
    #Use the route to send requests to a specific function
    
@mechanics_bp.route('/login', methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanics).where(Mechanics.email == email)
    customer = db.session.execute(query).scalars().first()
    
    if customer and customer.password == password:
        token = encode_token(customer.id)
        
        response = {
            'status': 'success',
            'message':'logged in successfully',
            'token':token
        }
        
        return jsonify(response), 200
    else:
        return jsonify({'message':'Invalid email or password!'})

@mechanics_bp.route('/',methods=['POST'])
@limiter.limit("5 per day")
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
# @cache.cached(timeout=20) #Used to save info in cache for faster retrieval.
def get_mechanics():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Mechanics)
        mechanics_all = db.paginate(query,page=page,per_page=per_page)
        return mechanics_schema.jsonify(mechanics_all)
        
    except:    
    
        query = select(Mechanics)
        mechanics_all = db.session.execute(query).scalars().all()
        
        return mechanics_schema.jsonify(mechanics_all), 200

    #Get specific customer
@mechanics_bp.route('/<int:mechanic_id>',methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic=db.session.get(Mechanics,mechanic_id)   
    
    if mechanic:
        return mechanic_schema.jsonify(mechanic),200
    return jsonify({'error':'Mechanic does not exist.'}),404

    #Update a customer (PUT)
@mechanics_bp.route('/', methods=['PUT'])
@token_required
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
@mechanics_bp.route('/', methods=['DELETE'])
@token_required
@limiter.limit("10 per day")
def delete_mechanic(mechanic_id):
    mechanic=db.session.get(Mechanics, mechanic_id)
    
    if not mechanic:
        return jsonify({'error','Mechanic does not exist'}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message':f'Mechanic id: {mechanic_id}, successfully deleted'}), 200


@mechanics_bp.route("/jobs",methods=['GET'])
def mech_jobs():
    query = select(Mechanics)
    mechanics = db.session.execute(query).scalars().all()
    
    mechanics.sort(key= lambda mechanic: len(mechanic.service_tickets),reverse=True)
    
    # for mechanic in mechanics:
    #     print(mechanic.name,len(mechanic.service_tickets))
    # print(mechanics)
    
    return mechanics_schema.jsonify(mechanics)

@mechanics_bp.route("/search",methods=['GET'])
def search_mech():
    mech_name = request.args.get("name")
    
    query  = select(Mechanics).where(Mechanics.name.like(f'%{mech_name}%')) #add the f function to optimize search
    mechanics = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics)