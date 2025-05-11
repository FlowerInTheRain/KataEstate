# Add the root of the project to sys.path
import csv
import logging
from logging.config import dictConfig

from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from db import Base, engine
from maintenances.mappers.from_csv import to_db_maintenance
from maintenances.repositories.CommandMaintenances import bulk_create_maintenances
from properties.mappers.with_id_to_db import from_csv
from properties.repositories.CommandProperties import bulk_create_properties
from properties.repositories.CommandProperties import cleanup_properties
from tenants.mappers.from_csv import to_db_tenant
from tenants.repositories.CommandTenants import bulk_create_tenants

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})




def create_app(testing=False):
    from properties.endpoints.properties_management import ns as properties_management_ns
    from healthcheck.endpoints.get_healthcheck import ns as healthcheck_ns

    healthcheck_paths = [healthcheck_ns]
    properties_paths = [properties_management_ns]
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}}, support_credentials=True,
         methods=["GET","POST", "PUT","DELETE", "OPTIONS"])
    logging.basicConfig(level=logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    api = Api(app, doc='/swagger', prefix='/api', mask_swagger=False)
    all_namespaces = (healthcheck_paths + properties_paths)
    for ns in all_namespaces:
        api.add_namespace(ns)

    with app.app_context():
        Base.metadata.create_all(bind=engine)
        if not testing:
            cleanup_properties()
            cleanup_properties()

            with open('resources/properties.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                properties = []
                for row in reader:
                    new_property = from_csv(row)
                    properties.append(new_property)
                bulk_create_properties(properties)

            with open('resources/tenants.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                tenants = []
                for row in reader:
                    new_tenant = to_db_tenant(row)
                    tenants.append(new_tenant)
                bulk_create_tenants(tenants)

            with open('resources/maintenance.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                maintenances = []
                for row in reader:
                    new_maintenance = to_db_maintenance(row)
                    maintenances.append(new_maintenance)
                bulk_create_maintenances(maintenances)

    app.logger.info("Database sanitized")
    return app




if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, use_debugger=True, use_reloader= False,host="0.0.0.0", port=5000)




