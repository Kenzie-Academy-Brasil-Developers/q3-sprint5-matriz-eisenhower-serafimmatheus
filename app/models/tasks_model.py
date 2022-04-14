from dataclasses import dataclass, asdict
from app.configs.database import db
from app.models.tasks_categories_model import tasks_categories_table


@dataclass
class TasksModel(db.Model):
    __TABLENAME__ = "tasks_model"

    id: int
    name: str
    description: str
    duration: int
    eisenhower: list

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)
    importance = db.Column(db.Integer)
    urgency = db.Column(db.Integer)
    eisenhower_id = db.Column(db.Integer, db.ForeignKey("eisenhower_model.id"), nullable=False)


    #relações
    eisenhower = db.relationship("EisenhowerModel", backref="task")

    
   