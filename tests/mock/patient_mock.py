from unittest.mock import MagicMock
from app.schemas.patient import ListPatientViewSchema, PatientViewSchema
from app.schemas.address import AddressSchema
from app.schemas.status import StatusResponseSchema


def mock_list_patients_success():
    mock = MagicMock()
    mock.return_value = ListPatientViewSchema(
        per_page=10,
        page=1,
        total=1,
        patients=[PatientViewSchema(
            id=1,
            name="John Doe",
            email="john.doe@example.com",
            phone="123456789",
            gender="Masculino",
            birth_date="1990-01-01",
            address=AddressSchema(
                zipcode="12345-678",
                address="Rua Exemplo",
                city="São Paulo",
                state="SP",
                neighborhood="string",
                number="100",
            ),
        )]
    )
    return mock


def mock_list_patients_failure_204():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=204,
        details="Nenhum paciente encontrado",
        message="Nenhum paciente encontrado"
    )
    return mock


def mock_list_patients_failure_500():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=500,
        details="Erro interno do servidor",
        message="Ocorreu um erro ao tentar listar os pacientes"
    )
    return mock


def mock_get_patient_success():
    mock = MagicMock()
    mock.return_value = PatientViewSchema(
        id=1,
        name="John Doe",
        email="john.doe@example.com",
        phone="123456789",
        gender="Masculino",
        birth_date="1990-01-01",
        address=AddressSchema(
            zipcode="12345-678",
            address="Rua Exemplo",
            city="São Paulo",
            state="SP",
            neighborhood="string",
            number="100",
        ),
    )
    return mock


def mock_get_patient_failure_404():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=404,
        details="Paciente não encontrado",
        message="Não foi possível encontrar o paciente"
    )
    return mock


def mock_get_patient_failure_500():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=500,
        details="Erro interno do servidor",
        message="Ocorreu um erro ao tentar obter o paciente"
    )
    return mock

def mock_update_patient_success():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=200,
        details=None,
        message="paciente atualizado com sucesso."
    )
    return mock


def mock_update_patient_failure_404():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=404,
        details="Paciente não encontrado",
        message="Não foi possível encontrar o paciente para atualizar"
    )
    return mock


def mock_update_patient_failure_500():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=500,
        details="Erro interno do servidor",
        message="Ocorreu um erro ao tentar atualizar o paciente"
    )
    return mock

def mock_create_patient_success():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=201,
        details=None,
        message="paciente criado com sucesso."
    )
    return mock

def mock_create_patient_failure_500():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=500,
        details="Erro interno do servidor",
        message="Ocorreu um erro ao tentar atualizar o paciente"
    )
    return mock


def mock_delete_patient_success():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=200,
        details=None,
        message="paciente deletado com sucesso."
    )
    return mock


def mock_delete_patient_failure_404():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=404,
        details="Paciente não encontrado",
        message="Não foi possível encontrar o paciente para deletar"
    )
    return mock


def mock_delete_patient_failure_500():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=500,
        details="Erro interno do servidor",
        message="Ocorreu um erro ao tentar deletar o paciente"
    )
    return mock
