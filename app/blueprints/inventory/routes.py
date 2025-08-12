
from marshmallow import ValidationError
from flask import request, jsonify
from sqlalchemy import select
from .inventorySchemas import inventory_schema, inventories_schema
from app.models import Inventory, db
from app.blueprints.inventory import inventory_bp
from app.utils.util import encode_token, token_required
from app.extensions import limiter


#Route creation:
    #Create inventory
    #Use the route to send requests to a specific function
    


@inventory_bp.route('/',methods=['POST'])
def create_inventory():
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # query = select(Inventory).where(inventory.data == inventory_data['email'])
    # existing_inventory = db.session.execute(query).scalars().all()
    # if existing_inventory:
    #     return jsonify({"error": "Email already exists"}), 404
    # new_inventory = inventory(**inventory_data)   #** unpacks the dictionary
    new_inventory = Inventory(inventory_name=inventory_data['inventory_name'], price=inventory_data['price'])
    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory), 201

    #Get all inventorys
@inventory_bp.route('/',methods=['GET'])
# @cache.cached(timeout=20)
def get_inventorys():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Inventory)
        inventories_all = db.paginate(query,page=page,per_page=per_page)
        return inventories_schema.jsonify(inventories_all), 200
    except:
        query = select(Inventory)
        inventories_all = db.session.execute(query).scalars().all()
        
        return inventories_schema.jsonify(inventories_all), 200

    #Get specific inventory
@inventory_bp.route('/<int:inventory_id>',methods=['GET'])
def get_inventory(inventory_id):
    inventory=db.session.get(inventory,inventory_id)   
    
    if inventory:
        return inventory_schema.jsonify(inventory),200
    return jsonify({'error':'inventory does not exist.'}),404

    #Update a inventory (PUT)
    #Now that we have the token required decorator, we could now remove the id in url that was once required.
    #Only logged in users have permissions to update their acct.
    
@inventory_bp.route('/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    inventory = db.session.get(Inventory,inventory_id)
    
    if not inventory:
        return jsonify({'error','inventory does not exist'}), 404
    
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for k, v in inventory_data.items():
        setattr(inventory,k,v)
    db.session.commit()
    return inventory_schema.jsonify(inventory),200    
    
    #Delete a inventory(DELETE)
    #Now that we have the token required decorator, we could now remove the id in url that was once required.
    #Only logged in users have permissions to delete their acct.
    
@inventory_bp.route('/<int:inventory_id>', methods=['DELETE'])
@limiter.limit("5 per day") #to limit request to 5 per day.
def delete_inventory(inventory_id):
    inventory=db.session.get(Inventory, inventory_id)
    query = select(Inventory.inventory_name).where(Inventory.id == inventory_id)
    inventory_name = db.session.execute(query).scalars().first()
    
    if not inventory:
        return jsonify({'error','inventory does not exist'}), 404
    
    db.session.delete(inventory)
    db.session.commit()
    return jsonify({'message':f'inventory ID: {inventory_id}, name: {inventory_name}, successfully deleted'}), 200

@inventory_bp.route("/search", methods=['GET'])
def search_inventory():
    inventory_name = request.args.get("inventory_name")
    query = select(Inventory).where(Inventory.inventory_name.like(f'%{inventory_name}%'))
    inventories = db.session.execute(query).scalars().all()
    
    return inventories_schema.jsonify(inventories)