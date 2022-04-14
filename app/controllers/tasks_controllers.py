from http import HTTPStatus
from sqlalchemy.orm import Session, Query
from flask import current_app, jsonify, request, session
from app.models.tasks_model import TasksModel
from app.models.categories_model import CategoriesModel
from app.models.tasks_categories_model import tasks_categories_table
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm.exc import FlushError


def create_tasks():
    session: Session = current_app.db.session
    data: dict = request.get_json()

    try:
        categorie_name = data.pop("categorie")
        
        categorie = []
        for name in categorie_name:
            categorie.append(session.query(CategoriesModel).filter_by(name=name).first())

        if data["importance"] == 1 and data["urgency"] == 1:
            data["eisenhower_id"] = 1
        elif data["importance"] == 1 and data["urgency"] == 2:
            data["eisenhower_id"] = 3
        elif data["importance"] == 2 and data["urgency"] == 1:
            data["eisenhower_id"] = 2
        elif data["importance"] == 2 and data["urgency"] == 2:
            data["eisenhower_id"] = 4

        tasks = TasksModel(**data)

        for cat in categorie:
            tasks.categories.append(cat)

        session.add(tasks)
        session.commit()

        return jsonify(tasks), HTTPStatus.CREATED

    except FlushError:
        return {"error": "category not exists"}, HTTPStatus.BAD_REQUEST
    except (TypeError, KeyError):
        expected = ["name", "description", "duration", "importance", "urgency", "categorie"]
        results = [key for key in data.keys()]
        return {"esperado": expected, "obtido": results}, HTTPStatus.CONFLICT



def get_all_tasks():
    session: Session = current_app.db.session

    tasks = session.query(TasksModel).all()

    []
    
    return jsonify(tasks), HTTPStatus.OK


def get_one_task(id: int):
    session: Session = current_app.db.session

    task = session.query(TasksModel).get(id)

    if not task:
        return {"error": f"id {id} not found"}, HTTPStatus.NOT_FOUND

    return jsonify(task), HTTPStatus.OK


def update_tasks(id: int):
    session: Session = current_app.db.session
    data: dict = request.get_json()

    try:
        task = session.query(TasksModel).get(id)

        if not task:
            return {"error": f"id {id} not found"}, HTTPStatus.NOT_FOUND

        if data.get("urgency") and data.get("importance"):
            if data["importance"] == 1 and data["urgency"] == 1:
                data["eisenhower_id"] = 1
            elif data["importance"] == 1 and data["urgency"] == 2:
                data["eisenhower_id"] = 3
            elif data["importance"] == 2 and data["urgency"] == 1:
                data["eisenhower_id"] = 2
            elif data["importance"] == 2 and data["urgency"] == 2:
                data["eisenhower_id"] = 4


        elif data.get("urgency"):
            if task.importance == 1 and data["urgency"] == 1:
                data["eisenhower_id"] = 1
            elif task.importance == 1 and data["urgency"] == 2:
                data["eisenhower_id"] = 3
            elif task.importance == 2 and data["urgency"] == 1:
                data["eisenhower_id"] = 2
            elif task.importance == 2 and data["urgency"] == 2:
                data["eisenhower_id"] = 4
        
        elif data.get("importance"):
            if data["importance"] == 1 and task.urgency == 1:
                data["eisenhower_id"] = 1
            elif data["importance"] == 1 and task.urgency == 2:
                data["eisenhower_id"] = 3
            elif data["importance"] == 2 and task.urgency == 1:
                data["eisenhower_id"] = 2
            elif data["importance"] == 2 and task.urgency == 2:
                data["eisenhower_id"] = 4
        

        if not task:
            return {"error": f"id {id} not found"}, HTTPStatus.NOT_FOUND

        for key, value in data.items():
            setattr(task, key, value)

        session.add(task)
        session.commit()

        return jsonify(task), HTTPStatus.OK

    except AttributeError:
        expected = ["name", "description", "duration", "importance", "urgency", "categorie"]
        results = [key for key in data.keys()]
        return {"esperado": expected , "obtido": results}, HTTPStatus.BAD_REQUEST
    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {"error": "name already exists"}, HTTPStatus.CONFLICT


def delete_tasks(id: int):
    session: Session = current_app.db.session

    task = session.query(TasksModel).get(id)

    if not task:
        return {"error": f"id {id} not found"}, HTTPStatus.NOT_FOUND

    session.delete(task)
    session.commit()

    return "", HTTPStatus.NO_CONTENT