from flask import Flask, Blueprint
from app.routes.categories_routes import bp as bp_categories
from app.routes.eisenhower_routes import bp as bp_eisenhower
from app.routes.tasks_routes import bp as bp_tasks


bp_api = Blueprint("api", __name__, url_prefix="")


def init_app(app: Flask):
    bp_api.register_blueprint(bp_categories)
    bp_api.register_blueprint(bp_eisenhower)
    bp_api.register_blueprint(bp_tasks)
    app.register_blueprint(bp_api)
