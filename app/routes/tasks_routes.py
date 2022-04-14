from flask import Blueprint
from app.controllers import tasks_controllers

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


bp.get("")(tasks_controllers.get_all_tasks)
bp.get("/<int:id>")(tasks_controllers.get_one_task)
bp.post("")(tasks_controllers.create_tasks)
bp.patch("/<int:id>")(tasks_controllers.update_tasks)
bp.delete("/<int:id>")(tasks_controllers.delete_tasks)