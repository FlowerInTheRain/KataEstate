from datetime import date, datetime

from flask import jsonify, request, current_app, Response
from flask_restx import Resource, Namespace, api, fields
from flask_restx.fields import Integer

from tenants.repositories import QueryTenants

from properties.models.PaymentStatuses import PaymentStatuses
from tenants.models.Tenants import Tenants, Tenant
from tenants.repositories import CommandTenants

ns = Namespace('tenants', description='CRUD Operations on tenants')

tenant_model = ns.model('Property', {
    'id': fields.Integer,
    'name': fields.String(required=True, min_length=5, max_length=50),
    'contact_info': fields.String(required=True, max_length=12,min_length=10),
    'lease_term_start': fields.String(required=True, min_length=10, max_length=10),
    'lease_term_end': fields.String(required=True, min_length=10, max_length=10),
    'rent_paid': fields.String(required=True, enum=[e.value for e in PaymentStatuses]),
    'property_id': fields.Integer(required=True)
})

add_tenant_model = ns.model('AddProperty', {
    'name': fields.String(required=True, min_length=5, max_length=50),
    'contact_info': fields.String(required=True, max_length=12,min_length=10),
    'lease_term_start': fields.String(required=True, min_length=10, max_length=10),
    'lease_term_end': fields.String(required=True, min_length=10, max_length=10),
    'rent_paid': fields.String(required=True, enum=[e.value for e in PaymentStatuses]),
    'property_id': fields.Integer(required=True)
})


@ns.route("/")
class BasePath(Resource):
    @ns.marshal_with(tenant_model, as_list=True)
    def get(self):  # put application's code here
        data = QueryTenants.get_all_tenants()
        for tenant in data:
            current_app.logger.info(tenant)
        return data

    @ns.expect(add_tenant_model, validate=True)
    def post(self):
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
            return CommandTenants.create_tenant(new_tenant)
        else:
            return Response(status=400)


    @ns.expect(tenant_model, validate=True)
    def put(self):
        current_tenant = from_json(request.json)
        start_date = date.fromisoformat(request.json["lease_term_start"])
        end_date = date.fromisoformat(request.json["lease_term_end"])
        if end_date > start_date:
            CommandTenants.update_tenant(current_tenant)
            return Response(status=204)
        else:
            return Response(status=400)


@ns.route('/<int:tenant_id>')
class ByID(Resource):
    def delete(self, tenant_id: Integer):
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
