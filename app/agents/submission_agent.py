import uuid
from datetime import datetime


class SubmissionAgent:

    def submit(self, authorization, validation_result):
        if validation_result["status"] != "VALID":
            return {
                "status": "NOT_SUBMITTED",
                "submission_id": None,
                "message": "Authorization failed validation.",
                "errors": validation_result["errors"],
                "warnings": validation_result["warnings"],
            }

        submission_id = f"AUTH-{uuid.uuid4().hex[:8].upper()}"

        return {
            "status": "SUBMITTED",
            "submission_id": submission_id,
            "submitted_at": datetime.now().isoformat(),
            "payer": authorization.payer.name,
            "patient": authorization.patient.name,
            "procedure": authorization.procedure.description,
            "message": "Authorization submitted successfully.",
        }