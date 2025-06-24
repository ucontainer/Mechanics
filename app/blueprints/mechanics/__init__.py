from flask import Blueprint

mechanics_bp = Blueprint("mechanics_bp", __name__)

#dont forget the below to import this blueprint to the app.__init__.py file to register it.
from . import routes