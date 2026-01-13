from pydantic import BaseModel

class CareerInput(BaseModel):
    experience: str
    employment: str
    company_size: str
    domain: str
