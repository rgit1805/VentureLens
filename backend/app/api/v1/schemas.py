from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    environment: str

class ErrorResponse(BaseModel):
    detail: str