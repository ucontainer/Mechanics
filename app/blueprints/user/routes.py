
from marshmallow import ValidationError
from flask import request, jsonify
from sqlalchemy import select
from .userSchemas import customer_schema, customers_schema
from app.models import Customer, db
from . import customers_bp


#Route creation:
    #Create customer
    #Use the route to send requests to a specific function
@customers_bp.route('/',methods=['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"error": "Email already exists"}), 404
    new_customer = Customer(**customer_data)   #** unpacks the dictionary
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

    #Get all customers
@customers_bp.route('/',methods=['GET'])
def get_customers():
    query = select(Customer)
    customers_all = db.session.execute(query).scalars().all()
    
    return customers_schema.jsonify(customers_all)

    #Get specific customer
@customers_bp.route('/<int:customer_id>',methods=['GET'])
def get_customer(customer_id):
    customer=db.session.get(Customer,customer_id)   
    
    if customer:
        return customer_schema.jsonify(customer),200
    return jsonify({'error':'Customer does not exist.'}),404

    #Update a customer (PUT)
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customer,customer_id)
    
    if not customer:
        return jsonify({'error','Customer does not exist'}), 404
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for k, v in customer_data.items():
        setattr(customer,k,v)
    db.session.commit()
    return customer_schema.jsonify(customer),200    
    
    #Delete a customer(DELETE)
@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer=db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({'error','Customer does not exist'}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message':f'Customer id: {customer_id}, successfully deleted'}), 200