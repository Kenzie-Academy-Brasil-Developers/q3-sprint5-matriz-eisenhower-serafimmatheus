from http import HTTPStatus
from flask import current_app, jsonify, request, session
from sqlalchemy.orm import Session
from app.models.eisenhower_model import EisenhowerModel


def get_all_eisenhower():
    session: Session = current_app.db.session

    eisenhower = session.query(EisenhowerModel).all()

    return jsonify(eisenhower), HTTPStatus.OK


def get_by_id_eisenhower(id: int):
    session: Session = current_app.db.session

    eisenhower = session.query(EisenhowerModel).get(id)

    if not eisenhower:
        return {"error": f"id {id} not found"}, HTTPStatus.NOT_FOUND

    return jsonify(eisenhower), HTTPStatus.OK


def create_eisenhower():
    session: Session = current_app.db.session
    data = request.get_json()

    eisenhower = EisenhowerModel(**data)

    session.add(eisenhower)
    session.commit()

    return jsonify(eisenhower), HTTPStatus.CREATED


def update_eisenhower(id: int):
    session: Session = current_app.db.session
    data: dict = request.get_json()

    eisenhower = session.query(EisenhowerModel).get(id)

    if not eisenhower:
        return {"error": f"id {id} not found"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(eisenhower, key, value)

    session.commit()

    return jsonify(eisenhower), HTTPStatus.OK



def delete_eisenhower(id: int):
    session: Session = current_app.db.session
    eisenhower = session.query(EisenhowerModel).get(id)

    if not eisenhower:
        return {"error": f"id {id} not found"}, HTTPStatus.NOT_FOUND


    session.delete(eisenhower)

    return "", HTTPStatus.NO_CONTENT