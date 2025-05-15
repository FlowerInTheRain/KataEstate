from datetime import date, datetime

from constants import API_base_path
from constants import CreateItemResponse
from flask import request, current_app, Blueprint
from flask_pydantic_spec import Request, Response
from flask_restx.fields import Integer
from properties.models.PaymentStatuses import PaymentStatuses
from tenants.models.Tenants import Tenants, Tenant
from tenants.models.dtos.TenantDTOs import TenantResponse, CreateTenant, UpdateTenant
from tenants.repositories import CommandTenants
from tenants.repositories import QueryTenants

from app import spec

tenants_blueprint = Blueprint('tenants management', __name__,
                                 url_prefix=API_base_path + '/tenants')


@tenants_blueprint.route("/", methods=["GET"])
@spec.validate(body=Request(), resp=Response(HTTP_200=TenantResponse))
def get_all_tenants():  # put application's code here
    data = QueryTenants.get_all_tenants()
    for tenant in data:
        current_app.logger.info(tenant)
    return [d.dict() for d in data],200

@tenants_blueprint.route("/", methods=["POST"])
@spec.validate(body=Request(CreateTenant), resp=Response(HTTP_201=CreateItemResponse))
def create_tenant():
    new_tenant = Tenants(
        request.json["name"],
        request.json["contact_info"],
        request.json["lease_term_start"],
        request.json["lease_term_end"],
        PaymentStatuses(request.json["rent_paid"]),
        request.json["property_id"])
    start_date = date.fromisoformat(request.json["lease_term_start"])
    end_date = date.fromisoformat(request.json["lease_term_end"])

    if end_date > start_date:
        return CommandTenants.create_tenant(new_tenant), 201
    else:
        return Response(status=400)


@tenants_blueprint.route("/", methods=["PUT"])
@spec.validate(body=Request(UpdateTenant), resp=Response())
def update_tenant():
    current_tenant = from_json(request.json)
    start_date = date.fromisoformat(request.json["lease_term_start"])
    end_date = date.fromisoformat(request.json["lease_term_end"])
    if end_date > start_date:
        CommandTenants.update_tenant(current_tenant)
        return Response(status=204)
    else:
        return Response(status=400)


@tenants_blueprint.route('/<int:tenant_id>', methods=["DELETE"])
def delete_tenant(tenant_id: Integer):
    CommandTenants.delete_tenant(tenant_id)
    return Response(status=204)

def from_json(json):
    mapped_tenant = Tenant()
    mapped_tenant.id = json["id"]
    mapped_tenant.name = json["name"]
    mapped_tenant.contact_info = json["contact_info"]
    mapped_tenant.lease_term_start = datetime.strptime(json["lease_term_start"], "%Y-%m-%d").date()
    mapped_tenant.lease_term_end = datetime.strptime(json["lease_term_end"], "%Y-%m-%d").date()
    mapped_tenant.rent_paid = PaymentStatuses(json["rent_paid"]).value
    mapped_tenant.property_id = json["property_id"]
    return mapped_tenant
