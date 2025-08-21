from app import create_app
from app.models import db

app = create_app('ProductionConfig')

    
with app.app_context():
    # db.drop_all()
    db.create_all()

# app.run(debug=True)
#App.run is not needed since gunicorn is running the app
#Name change from app.py to flask_app.py is so that gunicorn 
#   can differentiate from app folder. 