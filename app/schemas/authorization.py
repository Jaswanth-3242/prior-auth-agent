from pydantic import BaseModel


class Patient(BaseModel):
    name: str
    date_of_birth: str


class Provider(BaseModel):
    name: str


class Procedure(BaseModel):
    description: str


class Diagnosis(BaseModel):
    description: str


class Payer(BaseModel):
    name: str


class AuthorizationRequest(BaseModel):
    patient: Patient
    provider: Provider
    procedure: Procedure
    diagnosis: Diagnosis
    payer: Payer
    clinical_notes: str = ""