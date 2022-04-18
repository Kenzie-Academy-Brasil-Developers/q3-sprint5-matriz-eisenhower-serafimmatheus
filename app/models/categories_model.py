from dataclasses import dataclass, asdict
from app.configs.database import db
from app.models.tasks_categories_model import tasks_categories_table

@dataclass
class CategoriesModel(db.Model):
    __tablename__ = "categories"

    id: int
    name: str
    description: str
    tasks: list

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    tasks = db.relationship("TasksModel", secondary=tasks_categories_table, backref="categories")

    
    def asdict(self):
        return asdict(self)
