#this creates flask apps
from flask import Flask
from app.extensions import ma
from .models import db
from .blueprints.user import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import tickets_bp
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    #Initialize extensions
    ma.init_app(app)
    db.init_app(app)

    
    #Register blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    
    return app