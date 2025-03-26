from flask import jsonify
from logger import logger
from app.route import patient_tag
from app.schemas import PatientSaveSchema, PatientViewSchema
from app.schemas.patient import ListPatientViewSchema, IdPatientPathSchema
from app.schemas.filter import PatientFilterSchema
from app.schemas.status import StatusResponseSchema
from app.usecase.patient_usecase import PatientUseCase


class PatientRoute:

    def __init__(self):
        self.usecase = PatientUseCase()

    def init_routes(self, app):
        @app.post('/patient/list', tags=[patient_tag],
                  responses={
                      200: ListPatientViewSchema,
                      204: None,
                      500: StatusResponseSchema
                  })
        def list_patients_route(body: PatientFilterSchema):
            """Lista os pacientes cadastrados filtrando pelo nome."""
            logger.debug(f"Consultando o paciente: Buscando por [{body.name}]")
            response = self.usecase.list_patients(body)
            print(f"response: {response}")
            if isinstance(response, ListPatientViewSchema):
                logger.debug(f"Consultando o paciente [{body.name}]: Dados retornados")
                return jsonify(response.model_dump()), 200
            else:
                logger.debug(
                    f"Consultando o paciente: status code [{response.code}] - mensagem: ['{response.model_dump()}] '")
                return jsonify(response.model_dump()), response.code

        @app.get('/patient/<int:id_patient>', tags=[patient_tag],
                 responses={
                     200: PatientViewSchema,
                     404: StatusResponseSchema,
                     500: StatusResponseSchema
                 })
        def get_patient_route(path: IdPatientPathSchema):
            """Busca um paciente pelo ID."""
            logger.debug(f"Buscando o paciente de id: [{path.id_patient}]")
            response = self.usecase.get_patient(path.id_patient)
            if isinstance(response, PatientViewSchema):
                logger.debug(f"Buscando o paciente id:[{path.id_patient}]: Dados retornados")
                return jsonify(response.model_dump()), 200
            else:
                logger.debug(
                    f"Buscando o paciente: status code [{response.code}] - mensagem: [{response.model_dump()}]")
                return jsonify(response.model_dump()), response.code

        @app.post('/patient/create', tags=[patient_tag],
                  responses={
                      200: StatusResponseSchema,
                      400: StatusResponseSchema,
                      404: StatusResponseSchema,
                      500: StatusResponseSchema
                  })
        def create_patient_route(body: PatientSaveSchema):
            """Cria um novo paciente."""
            response = self.usecase.create_patient(body)
            logger.debug(f"Criando o paciente: status code [{response.code}] - mensagem: [{response.model_dump()}] '")
            return jsonify(response.model_dump()), response.code

        @app.put('/patient/<int:id_patient>', tags=[patient_tag],
                 responses={
                     200: StatusResponseSchema,
                     400: StatusResponseSchema,
                     404: StatusResponseSchema,
                     500: StatusResponseSchema
                 })
        def update_patient_route(path: IdPatientPathSchema, body: PatientSaveSchema):
            """Atualiza um paciente existente."""
            logger.debug(f"Alterando o paciente de id: [{path.id_patient}]")
            response = self.usecase.update_patient(path.id_patient, body)
            logger.debug(
                f"Atualizando o paciente: status code [{response.code}] - mensagem: [{response.model_dump()}]")
            return jsonify(response.model_dump()), response.code

        @app.delete('/patient/<int:id_patient>', tags=[patient_tag],
                    responses={
                        200: StatusResponseSchema,
                        404: StatusResponseSchema,
                        500: StatusResponseSchema
                    })
        def delete_patient_route(path: IdPatientPathSchema):
            """Exclui um paciente."""
            logger.debug(f"Excluindo o paciente de id: [{path.id_patient}]")
            response = self.usecase.delete_patient(path.id_patient)
            logger.debug(
                f"Excluindo o paciente: status code [{response.code}] - mensagem: [{response.model_dump()}]")
            return jsonify(response.model_dump()), response.code