from pydantic import BaseModel

class CareerInput(BaseModel):
    domain: str
    experience: str
    employment: str
    company_size: str
