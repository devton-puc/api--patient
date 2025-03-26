from pydantic import BaseModel, ConfigDict


class AddressSchema(BaseModel):
    """
    Define os Dados de endereço do cliente para Criar/Alterar o Cliente
    """
    zipcode: str
    address: str
    neighborhood: str
    city: str
    state: str
    number: str

    model_config = ConfigDict(from_attributes=True)