from datetime import datetime
from http import HTTPStatus
from flask import jsonify, request
from flask_sqlalchemy import BaseQuery
from app.models.lead_model import Lead
from app.configs.database import db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Query
import re


def create_lead():
    data = request.get_json()

    data["creation_date"] = datetime.now()
    data["last_visit"] = datetime.now()
    data["visits"] = 1

    pattern = r"^\([1-9]{2}\)[0-9]{5}\-[0-9]{4}$"   
    if re.fullmatch(pattern, data["phone"]) is not None:
        lead = Lead(**data)

        session: Session = db.session()
        session.add(lead)
        session.commit()

        return jsonify(lead), HTTPStatus.CREATED
    else:
        return {"error": "Telefone obrigatoriamente no formato (xx)xxxxx-xxxx"}, HTTPStatus.BAD_REQUEST

def get_leads():
    session: Session = db.session()
    base_query: BaseQuery = session.query(Lead)

    leads = base_query.order_by(Lead.visits).all()

    return jsonify(leads), HTTPStatus.OK

def update_lead():
    data = request.get_json()

    if len(data.keys()) != 1:
        return {"error": "Solicitação deve ser feita apenas com um email válido"}, HTTPStatus.BAD_REQUEST

    if type(data["email"]) is not str:
        return {"error": "Email inválido"}, HTTPStatus.BAD_REQUEST

    session: Session = db.session()
    lead = session.query(Lead).filter(data["email"]==Lead.email).first()

    if not lead:
        return {"error": "email não encontrado"}, HTTPStatus.NOT_FOUND  

    lead.visits += 1
    lead.last_visit = datetime.now()

    session.commit()

    return "", HTTPStatus.OK

def delete_lead():
    data = request.get_json()
    session: Session = db.session()

    lead = session.query(Lead).filter(data["email"]==Lead.email).first()

    if not lead:
        return {"error": "email não encontrado"}, HTTPStatus.NOT_FOUND

    session.delete(lead)
    session.commit()

    return "", HTTPStatus.OK
