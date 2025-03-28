from typing import List

from pydantic import BaseModel, EmailStr, ConfigDict

from app.schemas.address import AddressSchema


class PatientSaveSchema(BaseModel):
    """
    Define os Dados do Paciente para Criação/Alteração
    """
    name: str
    email: EmailStr
    phone: str
    gender: str
    birth_date: str
    address: AddressSchema

    model_config = ConfigDict(from_attributes=True)


class PatientViewSchema(BaseModel):
    """
    Define os Dados do Paciente para visualização
    """
    id: int
    name: str
    email: EmailStr
    phone: str
    gender: str
    birth_date: str
    address: AddressSchema

    model_config = ConfigDict(from_attributes=True)


class ListPatientViewSchema(BaseModel):
    """
    Define como uma listagem de pacientes será retornada.
    """
    per_page: int
    page: int
    total: int
    patients: List[PatientViewSchema]

    model_config = ConfigDict(from_attributes=True)


class IdPatientPathSchema(BaseModel):
    """
    Define objeto de busca
    """
    id_patient: int

    model_config = ConfigDict(from_attributes=True)
