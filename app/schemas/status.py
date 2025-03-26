from typing import Optional

from pydantic import BaseModel, ConfigDict


class StatusResponseSchema(BaseModel):
    """
    Define os Dados de status de requisição Sucesso / Falha
    """
    code: int
    message: str
    details: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
