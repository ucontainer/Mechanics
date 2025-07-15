
from marshmallow import ValidationError
from flask import request, jsonify
from sqlalchemy import select
from .userSchemas import customer_schema, customers_schema, login_schema
from app.models import Customer, db
from . import customers_bp
from app.utils.util import encode_token, token_required
from app.extensions import limiter, cache


#Route creation:
    #Create customer
    #Use the route to send requests to a specific function
    
@customers_bp.route('/login', methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == email)
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


@customers_bp.route('/',methods=['POST'])
@limiter.limit("5 per day") #to limit request to 5 per day.
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
# @cache.cached(timeout=20)
def get_customers():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Customer)
        customers_all = db.paginate(query,page=page,per_page=per_page)
        return customers_schema.jsonify(customers_all), 200
    except:
        query = select(Customer)
        customers_all = db.session.execute(query).scalars().all()
        
        return customers_schema.jsonify(customers_all), 200

    #Get specific customer
@customers_bp.route('/<int:customer_id>',methods=['GET'])
def get_customer(customer_id):
    customer=db.session.get(Customer,customer_id)   
    
    if customer:
        return customer_schema.jsonify(customer),200
    return jsonify({'error':'Customer does not exist.'}),404

    #Update a customer (PUT)
    #Now that we have the token required decorator, we could now remove the id in url that was once required.
    #Only logged in users have permissions to update their acct.
    
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@token_required
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
    #Now that we have the token required decorator, we could now remove the id in url that was once required.
    #Only logged in users have permissions to delete their acct.
    
@customers_bp.route('/', methods=['DELETE'])
@token_required
@limiter.limit("5 per day") #to limit request to 5 per day.
def delete_customer(customer_id):
    customer=db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({'error','Customer does not exist'}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message':f'Customer id: {customer_id}, successfully deleted'}), 200

@customers_bp.route("/search", methods=['GET'])
def search_customer():
    customer_name = request.args.get("name")
    query = select(Customer).where(Customer.name.like(f'%{customer_name}%'))
    customers = db.session.execute(query).scalars().all()
    
    return customers_schema.jsonify(customers)