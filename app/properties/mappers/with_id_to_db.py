from datetime import datetime

from properties.models.Properties import Property
from properties.models.PropertyStatuses import PropertyStatuses
from properties.models.PropertyTypes import PropertyTypes


def from_csv(row):
    new_property = Property()
    new_property.id = int(row[0])
    new_property.address = row[1]
    new_property.type = PropertyTypes(row[2]).value
    new_property.status = PropertyStatuses(row[3]).value
    new_property.purchase_date = datetime.strptime(row[4], "%Y-%m-%d").date()
    new_property.price = int(row[5]) * 100
    return new_property

def from_json(json: dict):
    property = Property()
    property.id = json["id"]
    property.address = json["address"]
    property.type = PropertyTypes(json["type"]).value
    property.status = PropertyStatuses(json["status"]).value
    property.purchase_date = datetime.strptime(json["purchase_date"], "%Y-%m-%d").date()
    property.price = json["price"] * 100
    return property