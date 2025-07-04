import jwt
from datetime import datetime, timedelta, timezone

#Tokens need expiration date. 
#Secret keys are used to sign and encode tokens specific to the applicaiton. 

SECRET_KEY = "super_secret_key"

def encode_token(user_id):
    payload = {
        'est':datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat':datetime.now(timezone.utc),
        'sub':user_id
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token