#this creates flask apps
from flask import Flask
from app.extensions import ma
from .models import db
from .blueprints.user import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import tickets_bp
from sqlalchemy.orm import DeclarativeBase
from .extensions import ma, limiter, cache
from .blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs' #URL for exposing SWAGGER UI without trailing '/'
API_URL = '/static/swagger.yaml' #Our API URL - can be a local resource.

swaggerui_blueprint=get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':'Mechanicx API'
    }
)

class Base(DeclarativeBase):
    pass

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    #Initialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    
    #Register blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(tickets_bp, url_prefix='/tickets')
    app.register_blueprint(inventory_bp,url_prefix='/inventory')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    return app