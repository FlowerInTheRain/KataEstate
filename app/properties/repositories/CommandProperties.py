from typing import List

from db import session
from flask import current_app
from properties.models.Properties import Properties
from properties.models.Properties import Property
from properties.repositories import QueryProperties
from sqlalchemy import Integer


def bulk_create_properties(properties: List[Property]):
    session.bulk_save_objects(properties)
    session.commit()

def create_property(new_property: Properties):
    to_db = Property()
    to_db.address = new_property.address
    to_db.type = new_property.type.value
    to_db.status = new_property.status.value
    to_db.purchase_date = new_property.purchase_date
    to_db.price = new_property.price
    to_db.id = None
    current_app.logger.info(to_db)
    session.add(to_db)
    session.commit()
    return to_db.id

def cleanup_properties():
    properties = QueryProperties.get_all_properties()

    # Delete all
    for in_db in properties:
        session.delete(in_db)

    session.commit()

def update_property(updated_property: Property):
    in_db = session.get(Property, updated_property.id)
    in_db.address = updated_property.address
    in_db.type = updated_property.type
    in_db.status = updated_property.status
    in_db.purchase_date = updated_property.purchase_date
    in_db.price = updated_property.price
    session.commit()


def delete_property(to_delete: Integer):
    in_db = session.get(Property, to_delete)
    session.delete(in_db)
    session.commit()
