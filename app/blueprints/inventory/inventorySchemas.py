from app.extensions import ma
from app.models import Inventory


class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
inventory_schema = InventorySchema()  #used to serialize a single Inventory object.
inventories_schema = InventorySchema(many=True)  #used to serialize many Inventory objects

