from http import HTTPStatus
from flask import current_app, jsonify, request
from sqlalchemy.orm import Session
from app.models.categories_model import CategoriesModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from psycopg2.errors import UniqueViolation


def get_all_categories():
    session: Session = current_app.db.session

    categories = session.query(CategoriesModel).all()

    serializer = [ 
        {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "tasks": [
                {
                    "id": task.id,
                    "name": task.name,
                    "description": task.description,
                    "duration": task.duration,
                    "classification": task.eisenhower.type
                }for task in category.tasks]
        } for category in categories 
    ]

    return jsonify(serializer)


def get_by_id_categories(id: int):
    session: Session = current_app.db.session

    categories = session.query(CategoriesModel).get(id)

    if not categories:
        return {"details": f"id {id} not found"}, HTTPStatus.NOT_FOUND

    return jsonify(categories), HTTPStatus.OK


def create_categories():
    session: Session = current_app.db.session

    try:
        data: dict = request.get_json()
        categories = CategoriesModel(**data)
        session.add(categories)
        session.commit()

        return jsonify(categories), HTTPStatus.CREATED
    
    except IntegrityError as e:
        return {"message": "category already exists!"}, HTTPStatus.CONFLICT
    except TypeError as e:
        expected = ["name", "description"]
        response = [key for key in data.keys()]

        return {"esperado": expected , "obtido": response}, HTTPStatus.BAD_REQUEST


def update_categories(id: int):
    session: Session = current_app.db.session

    try:
        data: dict = request.get_json()

        categories = session.query(CategoriesModel).get(id)

        for key, value in data.items():
            setattr(categories, key, value)

        session.commit()

        return jsonify(categories), HTTPStatus.OK

    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {"details": "category already exists!"}, HTTPStatus.CONFLICT
    except AttributeError:
        return {"details": "category not found!"}, HTTPStatus.NOT_FOUND
    except TypeError as e:
        expected = ["name", "description"]
        response = [key for key in data.keys()]

        return {"esperado": expected , "obtido": response}, HTTPStatus.BAD_REQUEST




def delete_categories(id: int):
    session: Session = current_app.db.session

    try:
        category = session.query(CategoriesModel).get(id)

        session.delete(category)
        session.commit()

        return "", HTTPStatus.NO_CONTENT
    except UnmappedInstanceError as e:
        return {"msg": "category not found!"}, HTTPStatus.NOT_FOUND