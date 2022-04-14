from flask import Blueprint
from app.controllers import categories_controllers


bp = Blueprint("categories", __name__, url_prefix="/categories")


bp.get("")(categories_controllers.get_all_categories)
bp.get("/<int:id>")(categories_controllers.get_by_id_categories)
bp.post("")(categories_controllers.create_categories)
bp.patch("/<int:id>")(categories_controllers.update_categories)
bp.delete("/<int:id>")(categories_controllers.delete_categories)

