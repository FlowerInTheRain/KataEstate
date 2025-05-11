from db import session

from properties.models.Properties import Property


def get_all_properties():
    return session.query(Property).order_by(Property.id).all()