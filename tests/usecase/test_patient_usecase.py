from unittest.mock import MagicMock, patch
import pytest
from app.model.patient import Patient
from app.model.address import Address
from app.usecase.patient_usecase import PatientUseCase
from sqlalchemy.exc import IntegrityError
from app.schemas.patient import PatientSaveSchema, ListPatientViewSchema, PatientViewSchema
from app.schemas.filter import PatientFilterSchema
from app.schemas.status import StatusResponseSchema
from app.schemas.address import AddressSchema

class TestPatientUseCase:

    @pytest.fixture
    def setup_usecase(self):
        return PatientUseCase()

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_return_list_patients_when_success(self, session_mock, setup_usecase):
        mock_address = MagicMock(spec=Address)
        mock_address.to_view_schema.return_value = {
            'zipcode': '12345-678',
            'address': 'Rua da Esperança',
            'neighborhood': 'Centro',
            'city': 'Rio de Janeiro',
            'state': 'RJ',
            'number': '123'
        }

        mock_patient_1 = MagicMock(spec=Patient)
        mock_patient_1.to_view_schema.return_value = {
            'id': 1,
            'name': 'John Doe',
            'personal_id': '12345678900',
            'email': 'johndoe@example.com',
            'phone': '999999999',
            'gender': 'Male',
            'birth_date': '1990-01-01',
            'address': mock_address.to_view_schema()
        }

        mock_patient_2 = MagicMock(spec=Patient)
        mock_patient_2.to_view_schema.return_value = {
            'id': 2,
            'name': 'Jane Smith',
            'personal_id': '12345678922',
            'email': 'janesmith@example.com',
            'phone': '888888888',
            'gender': 'Female',
            'birth_date': '1992-02-02',
            'address': mock_address.to_view_schema()
        }

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query  
        mock_query.count.return_value = 2  
        mock_query.offset.return_value.limit.return_value.all.return_value = [mock_patient_1, mock_patient_2]  # Lista de pacientes

        mock_session = session_mock.return_value
        mock_session.query.return_value = mock_query

        filter_patient = MagicMock()
        filter_patient.name = "John"
        filter_patient.page = 1
        filter_patient.per_page = 10

        response = setup_usecase.list_patients(filter_patient)

        assert isinstance(response, ListPatientViewSchema)
        assert response.total == 2
        assert response.page == 1
        assert response.per_page == 10
        assert len(response.patients) == 2


    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_return_list_patients_when_empty(self, session_mock, setup_usecase):

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query  
        mock_query.count.return_value = 0  
        mock_query.offset.return_value.limit.return_value.all.return_value = [] 

        mock_session = session_mock.return_value
        mock_session.query.return_value = mock_query

        filter_patient = MagicMock()
        filter_patient.name = "John"
        filter_patient.page = 1
        filter_patient.per_page = 10

        response = setup_usecase.list_patients(filter_patient)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 204
        assert response.message == "Paciente não encontrado."

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_return_list_patients_when_error(self, session_mock, setup_usecase):


        mock_patient_1 = MagicMock(spec=Patient)
        mock_patient_1.to_view_schema.return_value = {
            'id': 1,
            'name': 'John Doe',
            'personal_id': '12345678900',
            'email': 'johndoe@example.com',
            'phone': '999999999'
        }

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query  
        mock_query.count.return_value = 2  
        mock_query.offset.return_value.limit.return_value.all.return_value = [mock_patient_1]
        mock_session = session_mock.return_value
        mock_session.query.return_value = mock_query

        filter_patient = MagicMock()
        filter_patient.name = "John"
        filter_patient.page = 1
        filter_patient.per_page = 10

        response = setup_usecase.list_patients(filter_patient)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == 'Erro ao listar os pacientes'


    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_return_create_patient_when_success(self, session_mock, setup_usecase):

        mock_address = MagicMock(spec=Address)
        mock_address.zipcode = "12345-678"
        mock_address.address = "Rua da Esperança"
        mock_address.neighborhood = "Centro"
        mock_address.city = "Rio de Janeiro"
        mock_address.state = "RJ"
        mock_address.number = "123"

        mock_patient = MagicMock(spec=Patient)
        mock_patient.name = "John Doe"
        mock_patient.personal_id = "12345678900"
        mock_patient.email = "johndoe@example.com"
        mock_patient.phone = "999999999"
        mock_patient.gender = "Male"
        mock_patient.birth_date = "01/01/2000"
        mock_patient.address = mock_address

        mock_session = session_mock.return_value
        mock_session.add.return_value = None 
        mock_session.commit.return_value = None 

        patient_data = MagicMock()
        patient_data.name = "John Doe"
        patient_data.personal_id = "12345678900"
        patient_data.email = "johndoe@example.com"
        patient_data.phone = "999999999"
        patient_data.gender = "Male"
        patient_data.birth_date = "01/01/2000"
        patient_data.address = MagicMock()
        patient_data.address.zipcode = "12345-678"
        patient_data.address.address = "Rua da Esperança"
        patient_data.address.neighborhood = "Centro"
        patient_data.address.city = "Rio de Janeiro"
        patient_data.address.state = "RJ"
        patient_data.address.number = "123"

        response = setup_usecase.create_patient(patient_data)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 201
        assert response.message == "paciente criado com sucesso."

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_create_patient_when_error(self, session_mock, setup_usecase):

        mock_address = MagicMock(spec=Address)
        mock_address.zipcode = "12345-678"
        mock_address.address = "Rua da Esperança"
        mock_address.neighborhood = "Centro"
        mock_address.city = "Rio de Janeiro"
        mock_address.state = "RJ"
        mock_address.number = "123"

        mock_patient = MagicMock(spec=Patient)
        mock_patient.name = "John Doe"
        mock_patient.personal_id = "12345678900"
        mock_patient.email = "johndoe@example.com"
        mock_patient.phone = "999999999"
        mock_patient.gender = "Male"
        mock_patient.birth_date = "01/01/2000"
        mock_patient.address = mock_address

        mock_session = session_mock.return_value
        mock_session.add.return_value = None 
        mock_session.commit.return_value = None 

        patient_data = MagicMock()
        patient_data.name = "John Doe"
        patient_data.personal_id = "12345678900"
        patient_data.email = "johndoe@example.com"
        patient_data.phone = "999999999"
        patient_data.gender = "Male"
        patient_data.birth_date = ""
        patient_data.address = MagicMock()
        patient_data.address.zipcode = "12345-678"
        patient_data.address.address = "Rua da Esperança"
        patient_data.address.neighborhood = "Centro"
        patient_data.address.city = "Rio de Janeiro"
        patient_data.address.state = "RJ"
        patient_data.address.number = "123"

        response = setup_usecase.create_patient(patient_data)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == "Erro ao Criar o paciente"

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_create_patient_when_error_exists(self, session_mock, setup_usecase):

        mock_address = MagicMock(spec=Address)
        mock_address.zipcode = "12345-678"
        mock_address.address = "Rua da Esperança"
        mock_address.neighborhood = "Centro"
        mock_address.city = "Rio de Janeiro"
        mock_address.state = "RJ"
        mock_address.number = "123"

        mock_patient = MagicMock(spec=Patient)
        mock_patient.name = "John Doe"
        mock_patient.personal_id = "12345678900"
        mock_patient.email = "johndoe@example.com"
        mock_patient.phone = "999999999"
        mock_patient.gender = "Male"
        mock_patient.birth_date = "01/01/2000"
        mock_patient.address = mock_address

        mock_session = session_mock.return_value
        mock_session.add.return_value = None 
        mock_session.commit.return_value = None 

        patient_data = MagicMock()
        patient_data.name = "John Doe"
        patient_data.personal_id = "12345678900"
        patient_data.email = "johndoe@example.com"
        patient_data.phone = "999999999"
        patient_data.gender = "Male"
        patient_data.birth_date = "01/01/2000"
        patient_data.address = MagicMock()
        patient_data.address.zipcode = "12345-678"
        patient_data.address.address = "Rua da Esperança"
        patient_data.address.neighborhood = "Centro"
        patient_data.address.city = "Rio de Janeiro"
        patient_data.address.state = "RJ"
        patient_data.address.number = "123"

        mock_session = session_mock.return_value
        mock_session.add.return_value = None
        mock_session.commit.side_effect = IntegrityError("Erro de integridade", None, None)
        response = setup_usecase.create_patient(patient_data)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == "Erro ao Criar o paciente"
        assert response.details == "Dados informados já existem"

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_update_patient_when_success(self, session_mock, setup_usecase):

        mock_address = MagicMock(spec=Address)
        mock_address.zipcode = "12345-678"
        mock_address.address = "Rua Atualizada"
        mock_address.neighborhood = "Centro Atualizado"
        mock_address.city = "São Paulo"
        mock_address.state = "SP"
        mock_address.number = "456"

        mock_patient = MagicMock(spec=Patient)
        mock_patient.name = "John Doe"
        mock_patient.personal_id = "12345678900"
        mock_patient.email = "johndoe@example.com"
        mock_patient.phone = "999999999"
        mock_patient.gender = "Male"
        mock_patient.birth_date = "02/02/1992"
        mock_patient.address = mock_address

        mock_session = session_mock.return_value
        mock_session.query.return_value.get.return_value = mock_patient
        mock_session.commit.return_value = None

        patient_data = MagicMock()
        patient_data.name = "Jane Doe"
        patient_data.personal_id = "12345678922"
        patient_data.email = "janedoe@example.com"
        patient_data.phone = "888888888"
        patient_data.gender = "Female"
        patient_data.birth_date = "02/02/1992"
        patient_data.address = MagicMock()
        patient_data.address.zipcode = "12345-678"
        patient_data.address.address = "Rua Atualizada"
        patient_data.address.neighborhood = "Centro Atualizado"
        patient_data.address.city = "São Paulo"
        patient_data.address.state = "SP"
        patient_data.address.number = "456"

        response = setup_usecase.update_patient(1, patient_data)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 200
        assert response.message == "paciente alterado com sucesso."

        mock_session.commit.assert_called_once()

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_update_patient_when_not_found(self, session_mock, setup_usecase):

        mock_session = session_mock.return_value
        mock_session.query.return_value.get.return_value = None
        mock_session.commit.return_value = None

        patient_data = MagicMock()
        patient_data.name = "Jane Doe"
        patient_data.personal_id = "12345678922"
        patient_data.email = "janedoe@example.com"
        patient_data.phone = "888888888"
        patient_data.gender = "Female"
        patient_data.birth_date = "02/02/1992"
        patient_data.address = MagicMock()
        patient_data.address.zipcode = "12345-678"
        patient_data.address.address = "Rua Atualizada"
        patient_data.address.neighborhood = "Centro Atualizado"
        patient_data.address.city = "São Paulo"
        patient_data.address.state = "SP"
        patient_data.address.number = "456"

        response = setup_usecase.update_patient(1, patient_data)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 404
        assert response.message == "Paciente não encontrado."

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_update_patient_when_error(self, session_mock, setup_usecase):

        mock_patient = MagicMock(spec=Patient)
        mock_patient.name = "John Doe"
        mock_patient.personal_id = "12345678900"
        mock_patient.email = "johndoe@example.com"
        mock_patient.phone = "999999999"

        mock_session = session_mock.return_value
        mock_session.query.return_value.get.return_value = mock_patient
        mock_session.commit.return_value = None

        patient_data = MagicMock()
        patient_data.name = "Jane Doe"
        patient_data.personal_id = "12345678922"
        patient_data.address.address = "Rua Atualizada"
        patient_data.address.neighborhood = "Centro Atualizado"
        patient_data.address.city = "São Paulo"
        patient_data.address.state = "SP"
        patient_data.address.number = "456"

        response = setup_usecase.update_patient(1, patient_data)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == "Erro ao Alterar o paciente"

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_delete_patient_when_success(self, session_mock, setup_usecase):
  
        mock_patient = MagicMock(spec=Patient)
        mock_patient.id = 1
        mock_patient.name = "John Doe"

        mock_session = session_mock.return_value
        mock_session.query.return_value.get.return_value = mock_patient
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None

        response = setup_usecase.delete_patient(1)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 200
        assert response.message == "paciente excluído com sucesso."

        mock_session.delete.assert_called_once_with(mock_patient)
        mock_session.commit.assert_called_once()

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_delete_patient_when_not_found(self, session_mock, setup_usecase):
  
        mock_session = session_mock.return_value
        mock_session.query.return_value.get.return_value = None
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None

        response = setup_usecase.delete_patient(1)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 404
        assert response.message == "paciente não encontrado."

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_delete_patient_when_error(self, session_mock, setup_usecase):
  
        mock_patient = MagicMock(spec=Patient)
        mock_patient.id = 1
        mock_patient.name = "John Doe"

        mock_session = session_mock.return_value
        mock_session.query.return_value.get.return_value = mock_patient
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None

        mock_session.delete.side_effect = Exception("Erro ao excluir o paciente")

        response = setup_usecase.delete_patient(1)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == "Erro ao excluir o paciente"       

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_return_patient_when_success(self, session_mock, setup_usecase):

        mock_address = MagicMock(spec=Address)
        mock_address.to_view_schema.return_value = {
            'zipcode': '12345-678',
            'address': 'Rua da Esperança',
            'neighborhood': 'Centro',
            'city': 'Rio de Janeiro',
            'state': 'RJ',
            'number': '123'
        }

        mock_patient = MagicMock(spec=Patient)
        mock_patient.to_view_schema.return_value = {
            'id': 1,
            'name': 'John Doe',
            'personal_id': '12345678922',
            'email': 'johndoe@example.com',
            'phone': '999999999',
            'gender': 'Male',
            'birth_date': '1990-01-01',
            'address': mock_address.to_view_schema()
        }

        mock_session = session_mock.return_value
        mock_session.get.return_value = mock_patient

        response = setup_usecase.get_patient(1)

        assert isinstance(response, PatientViewSchema)
        assert response.id == 1
        assert response.name == 'John Doe'
        assert response.personal_id == "12345678922"
        assert response.address.zipcode == '12345-678'

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_return_patient_when_not_found(self, session_mock, setup_usecase):

        mock_session = session_mock.return_value
        mock_session.get.return_value = None

        response = setup_usecase.get_patient(1)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 404
        assert response.message == 'paciente não encontrado.'

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_return_patient_when_error(self, session_mock, setup_usecase):

        mock_patient = MagicMock(spec=Patient)
        mock_patient.to_view_schema.return_value = {
            'id': 1,
            'name': 'John Doe',
            'email': 'johndoe@example.com',
        }

        mock_session = session_mock.return_value
        mock_session.get.return_value = mock_patient

        response = setup_usecase.get_patient(1)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == 'Erro ao obter o paciente'


    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_return_patient_personal_id_when_success(self, session_mock, setup_usecase):

        mock_address = MagicMock(spec=Address)
        mock_address.to_view_schema.return_value = {
            'zipcode': '12345-678',
            'address': 'Rua da Esperança',
            'neighborhood': 'Centro',
            'city': 'Rio de Janeiro',
            'state': 'RJ',
            'number': '123'
        }

        mock_patient = MagicMock(spec=Patient)
        mock_patient.to_view_schema.return_value = {
            'id': 1,
            'name': 'John Doe',
            'personal_id': '12345678922',
            'email': 'johndoe@example.com',
            'phone': '999999999',
            'gender': 'Male',
            'birth_date': '1990-01-01',
            'address': mock_address.to_view_schema()
        }

        mock_session = session_mock.return_value
        mock_session.query.return_value.filter.return_value.first.return_value = mock_patient

        response = setup_usecase.get_patient_personal_id("12345678900")

        assert isinstance(response, PatientViewSchema)
        assert response.id == 1
        assert response.name == 'John Doe'
        assert response.personal_id == "12345678922"
        assert response.address.zipcode == '12345-678'

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_return_patient_personal_id_when_not_found(self, session_mock, setup_usecase):

        mock_session = session_mock.return_value
        mock_session.query.return_value.filter.return_value.first.return_value = mock_patient = None

        response = setup_usecase.get_patient_personal_id("12345678900")

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 404
        assert response.message == 'paciente não encontrado.'

    @patch("app.usecase.patient_usecase.SessionLocal")
    def test_should_return_patient_personal_id_when_error(self, session_mock, setup_usecase):

        mock_patient = MagicMock(spec=Patient)
        mock_patient.to_view_schema.return_value = {
            'id': 1,
            'name': 'John Doe',
            'email': 'johndoe@example.com',
        }

        mock_session = session_mock.return_value
        mock_session.query.filter.first.return_value = mock_patient

        response = setup_usecase.get_patient_personal_id("12345678900")

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == 'Erro ao obter o paciente'
