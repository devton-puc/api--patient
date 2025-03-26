from flask_openapi3 import OpenAPI, Info, APIBlueprint
from flask_cors import CORS

from app.model import init_db
from app.route.patient_route import PatientRoute

info = Info(title="Patient API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

init_db()

PatientRoute().init_routes(app)

