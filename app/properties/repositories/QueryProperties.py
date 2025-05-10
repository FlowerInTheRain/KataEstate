from db import session
from flask import current_app

from properties.models.Properties import Property


def get_all_properties():
    current_app.logger.info(session.query(Property).all())
    return session.query(Property).all()