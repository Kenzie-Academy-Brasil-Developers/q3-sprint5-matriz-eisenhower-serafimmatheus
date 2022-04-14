from flask import Blueprint
from app.controllers import eisenhower_controllers


bp = Blueprint("eisenhower", __name__, url_prefix="/eisenhower")


bp.get("")(eisenhower_controllers.get_all_eisenhower)
bp.get("/<int:id>")(eisenhower_controllers.get_by_id_eisenhower)
bp.post("")(eisenhower_controllers.create_eisenhower)
bp.patch("/<int:id>")(eisenhower_controllers.update_eisenhower)
bp.delete("/<int:id>")(eisenhower_controllers.delete_eisenhower)