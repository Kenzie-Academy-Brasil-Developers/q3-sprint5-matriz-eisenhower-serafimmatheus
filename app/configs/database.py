from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)

    app.db = db

    #imports das models
    from app.models.categories_model import CategoriesModel
    from app.models.eisenhower_model import EisenhowerModel
    from app.models.tasks_model import TasksModel
    from app.models.tasks_categories_model import tasks_categories_table
