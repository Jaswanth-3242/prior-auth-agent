from dataclasses import dataclass


@dataclass
class AuthorizationRecord:
    submission_id: str
    patient_name: str
    payer: str
    procedure: str
    status: str
    submitted_at: str
    updated_at: str