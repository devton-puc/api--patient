from sqlalchemy.exc import IntegrityError
from app.model import SessionLocal
from app.model.address import Address
from app.model.patient import Patient
from app.schemas.patient import PatientSaveSchema, ListPatientViewSchema, PatientViewSchema
from app.schemas.filter import PatientFilterSchema
from app.schemas.status import StatusResponseSchema
from app.schemas.address import AddressSchema
from app.utils.date_utils import parse_date, format_date 

class PatientUseCase:

    def list_patients(self, filter_patient: PatientFilterSchema) -> ListPatientViewSchema | StatusResponseSchema:
        try:
            session = SessionLocal()
            query = session.query(Patient)

            if filter_patient.name:
                query = query.filter(Patient.name.like(f'%{filter_patient.name}%'))

            total = query.count()
            patients = query.offset((filter_patient.page - 1) * filter_patient.per_page).limit(
                filter_patient.per_page).all()

            if not patients:
                return StatusResponseSchema(code=204, message="Paciente não encontrado.")

            return ListPatientViewSchema(total=total, page=filter_patient.page, per_page=filter_patient.per_page,
                                          patients=[patient.to_view_schema() for patient in patients])

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao listar os pacientes", details=f"{error}")


    def create_patient(self, patient_data: PatientSaveSchema) -> StatusResponseSchema:

        try:
            session = SessionLocal()

            new_patient = Patient(
                name=patient_data.name,
                personal_id=patient_data.personal_id,
                email=patient_data.email,
                phone=patient_data.phone,
                gender=patient_data.gender,
                birth_date=parse_date(patient_data.birth_date)
            )

            if patient_data.address:
                new_patient.address=Address(
                    zipcode=patient_data.address.zipcode,
                    address=patient_data.address.address,
                    neighborhood=patient_data.address.neighborhood,
                    city=patient_data.address.city,
                    state=patient_data.address.state,
                    number=patient_data.address.number
                )


            session.add(new_patient)
            session.commit()

            return StatusResponseSchema(code=201, message="paciente criado com sucesso.")

        except IntegrityError as error:
            return StatusResponseSchema(code=500, message="Erro ao Criar o paciente",
                                        details="Dados informados já existem")

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao Criar o paciente", details=f"{error}")

    def update_patient(self, id: int, patient_data: PatientSaveSchema) -> StatusResponseSchema:

        try:

            session = SessionLocal()
            patient = session.query(Patient).get(id)
            if not patient:
                return StatusResponseSchema(code=404, message="Paciente não encontrado.")

            if patient_data.name:
                patient.name = patient_data.name
            if patient_data.personal_id:
                patient.personal_id = patient_data.personal_id
            if patient_data.email:
                patient.email = patient_data.email
            if patient_data.phone:
                patient.phone = patient_data.phone
            if patient_data.gender:
                patient.gender = patient_data.gender
            if patient_data.birth_date:
                patient.birth_date = parse_date(patient_data.birth_date)

            if patient_data.address:
                patient.address.zipcode = patient_data.address.zipcode
                patient.address.address = patient_data.address.address
                patient.address.neighborhood = patient_data.address.neighborhood
                patient.address.city = patient_data.address.city
                patient.address.state = patient_data.address.state
                patient.address.number = patient_data.address.number

            session.commit()
            return StatusResponseSchema(code=200, message="paciente alterado com sucesso.")

        except IntegrityError as error:
            return StatusResponseSchema(code=500, message="Os dados informados já existem",
                                        details="")

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao Alterar o paciente", details=f"{error}")

    def delete_patient(self, id: int) -> StatusResponseSchema:
        try:

            session = SessionLocal()
            patient = session.query(Patient).get(id)
            if not patient:
                return StatusResponseSchema(code=404, message="paciente não encontrado.")

            session.delete(patient)
            session.commit()
            return StatusResponseSchema(code=200, message="paciente excluído com sucesso.")

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao excluir o paciente", details=f"{error}")


    def get_patient(self, id: int) -> PatientViewSchema | StatusResponseSchema:

        try:

            session = SessionLocal()
            patient = session.get(Patient, id)
            print(f'passou {patient}')
            if not patient:
                return StatusResponseSchema(code=404, message="paciente não encontrado.")
            return PatientViewSchema(**patient.to_view_schema())

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao obter o paciente", details=f"{error}")


