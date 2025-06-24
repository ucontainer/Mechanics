from flask import Blueprint

customers_bp = Blueprint("customers_bp", __name__)

#dont forget the below to import this blueprint to the app.__init__.py file to register it.
from . import routes