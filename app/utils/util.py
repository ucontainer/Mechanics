import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify

#Tokens need expiration date. 
#Secret keys are used to sign and encode tokens specific to the applicaiton. 

SECRET_KEY = "super_secret_key"

def encode_token(user_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        'iat': datetime.now(timezone.utc),  # iat - issued at.
        'sub': user_id
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    # Ensure the token is a string (PyJWT >= 2.x returns bytes)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

#Wrapper sitting on function needs to access the request that triggers the route.
#Token (Auth header) will be embeded in the request. So you'll need to access request to check for the token.
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1] #request headers comes as ['bearer','token string']. So get index [1].
            if not token:
                return jsonify({'message':'missing token'}), 400
            try:
                data = jwt.decode(token,SECRET_KEY, algorithms='HS256')
                print(data)
                user_id = data['sub']
            except jwt.ExpiredSignature as e:
                return jsonify({'message':'token expired'}), 400
            except jwt.InvalidTokenError as e:
                return jsonify({'message':'invalid token'}), 400    
            
            return f(user_id, *args, **kwargs)    
        else:
            return jsonify({'message':'please login to access.'}), 400    
    
    #when wrapper is called, decorated function 'f(user_id, *args, **kwargs)' is called
    return decorated     