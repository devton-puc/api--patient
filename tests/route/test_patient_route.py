import pytest
from unittest.mock import patch, MagicMock
from app import app
from tests.mock.patient_mock import (
    mock_list_patients_success,
    mock_list_patients_failure_204,
    mock_list_patients_failure_500,
    mock_get_patient_success,
    mock_get_patient_failure_404,
    mock_get_patient_failure_500,
    mock_create_patient_success,
    mock_create_patient_failure_500,
    mock_update_patient_success,
    mock_update_patient_failure_404,
    mock_update_patient_failure_500,
    mock_delete_patient_success,
    mock_delete_patient_failure_404,
    mock_delete_patient_failure_500,
)


@pytest.fixture
def client():
    """Mocka a sessão do banco e retorna um cliente de teste do Flask"""
    with patch("app.model.SessionLocal", MagicMock()):
        app.testing = True
        with app.test_client() as client:
            yield client


class TestPatientRoute:

    def test_should_return_http200_list_patients_when_success(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.list_patients", mock_list_patients_success()):
            filter_data = {
                "page": 1,
                "per_page": 5,
                "name": ""
            }
            response = client.post("/patient/list", json=filter_data)
            assert response.status_code == 200
            assert 'patients' in response.json

    def test_should_return_http204_list_patients_when_no_patients_found(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.list_patients", mock_list_patients_failure_204()):
            filter_data = {
                "page": 1,
                "per_page": 5,
                "name": ""
            }
            response = client.post("/patient/list", json=filter_data)
            assert response.status_code == 204

    def test_should_return_http500_list_patients_when_error(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.list_patients", mock_list_patients_failure_500()):
            filter_data = {
                "page": 1,
                "per_page": 5,
                "name": ""
            }
            response = client.post("/patient/list", json=filter_data)
            assert response.status_code == 500

    def test_should_return_http200_get_patient_when_success(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.get_patient", mock_get_patient_success()):
            response = client.get("/patient/1")
            assert response.status_code == 200
            assert 'id' in response.json

    def test_should_return_http404_get_patient_when_not_found(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.get_patient", mock_get_patient_failure_404()):
            response = client.get("/patient/1")
            assert response.status_code == 404

    def test_should_return_http500_get_patient_when_error(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.get_patient", mock_get_patient_failure_500()):
            response = client.get("/patient/1")
            assert response.status_code == 500

    def test_should_return_http200_get_patient_personal_id_when_success(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.get_patient_personal_id", mock_get_patient_success()):
            response = client.get("/patient/personal-id/12345678900")
            assert response.status_code == 200
            assert 'id' in response.json

    def test_should_return_http404_get_patient_personal_id_when_not_found(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.get_patient_personal_id", mock_get_patient_failure_404()):
            response = client.get("/patient/personal-id/12345678900")
            assert response.status_code == 404

    def test_should_return_http500_get_patient_personal_id_when_error(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.get_patient_personal_id", mock_get_patient_failure_500()):
            response = client.get("/patient/personal-id/12345678900")
            assert response.status_code == 500

    #--------------------------------------

    def test_should_return_http200_create_patient_when_success(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.create_patient", mock_create_patient_success()):
            new_patient = {
                "name": "Joana Dark",
                "personal_id": "12345678922",                
                "email": "joana.dark@email.com",
                "phone": "2133448866",
                "gender": "female",
                "birth_date": "22/02/1990", 
                "address": {
                    "zipcode": "12345",
                    "address": "123 Main St",
                    "neighborhood": "Central",
                    "city": "Springfield",
                    "state": "IL",
                    "number": "10"
                }
            }
            response = client.post("/patient/create", json=new_patient)
            assert response.status_code == 201

    def test_should_return_http400_create_patient_when_error(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.create_patient", mock_create_patient_failure_500()):
            new_patient = {
                "name": "Joana Dark",
                "personal_id": "12345678922",                
                "email": "joana.dark@email.com",
                "phone": "2133448866",
                "gender": "female",
                "birth_date": "22/02/1990",  
                "address": {
                    "zipcode": "12345",
                    "address": "123 Main St",
                    "neighborhood": "Central",
                    "city": "Springfield",
                    "state": "IL",
                    "number": "10"
                }
            }
            response = client.post("/patient/create", json=new_patient)
            assert response.status_code == 500

    def test_should_return_http404_update_patient_when_not_found(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.update_patient", mock_update_patient_failure_404()):
            updated_patient = {
                "name": "Joana Gomes",
                "personal_id": "12345678911",                
                "email": "joana.gomes@email.com",
                "phone": "2199448866",
                "gender": "female",
                "birth_date": "22/02/1970", 
                "address": {
                    "address": "updated_address",
                    "city": "updated_city",
                    "neighborhood": "updated_neighborhood",
                    "number": "updated_number",
                    "state": "updated_state",
                    "zipcode": "updated_zipcode"
                }
            }
            response = client.put("/patient/999", json=updated_patient)
            assert response.status_code == 404

    def test_should_return_http500_update_patient_when_error(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.update_patient", mock_update_patient_failure_500()):
            updated_patient = {
                "name": "Joana Gomes",
                "personal_id": "12345678911",                
                "email": "joana.gomes@email.com",
                "phone": "2199448866",
                "gender": "female",
                "birth_date": "22/02/2000",
                "address": {
                    "address": "updated_address",
                    "city": "updated_city",
                    "neighborhood": "updated_neighborhood",
                    "number": "updated_number",
                    "state": "updated_state",
                    "zipcode": "updated_zipcode"
                }
            }
            response = client.put("/patient/1", json=updated_patient)
            assert response.status_code == 500

    def test_should_return_http200_delete_patient_when_success(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.delete_patient", mock_delete_patient_success()):
            response = client.delete("/patient/1")
            assert response.status_code == 200

    def test_should_return_http404_delete_patient_when_not_found(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.delete_patient", mock_delete_patient_failure_404()):
            response = client.delete("/patient/999")
            assert response.status_code == 404

    def test_should_return_http500_delete_patient_when_error(self, client):
        with patch("app.usecase.patient_usecase.PatientUseCase.delete_patient", mock_delete_patient_failure_500()):
            response = client.delete("/patient/1")
            assert response.status_code == 500