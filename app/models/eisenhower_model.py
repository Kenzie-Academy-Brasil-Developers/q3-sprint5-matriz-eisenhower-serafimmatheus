from dataclasses import dataclass
from app.configs.database import db


@dataclass
class EisenhowerModel(db.Model):
    __TABLENAME__ = "eisenhower_model"

    id: int
    type: str

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))

    