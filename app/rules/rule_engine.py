class RuleEngine:

    def validate(self, authorization, payer_rules: str) -> dict:
        errors = []
        warnings = []

        # -------------------------
        # Basic required fields
        # -------------------------

        if not authorization.patient.name:
            errors.append("Patient name is missing.")

        if not authorization.patient.date_of_birth:
            errors.append("Patient date of birth is missing.")

        if not authorization.provider.name:
            errors.append("Provider name is missing.")

        if not authorization.procedure.description:
            errors.append("Procedure description is missing.")

        if not authorization.diagnosis.description:
            errors.append("Diagnosis description is missing.")

        if not authorization.payer.name:
            errors.append("Payer name is missing.")

        # -------------------------
        # Clinical documentation
        # -------------------------

        clinical_notes = authorization.clinical_notes.lower()

        if not clinical_notes:
            errors.append(
                "Clinical documentation is missing."
            )
        else:

            if not any(
                keyword in clinical_notes
                for keyword in [
                    "duration",
                    "weeks",
                    "months",
                    "persistent",
                    "chronic"
                ]
            ):
                warnings.append(
                    "Duration or severity of symptoms "
                    "may not be documented."
                )

            if not any(
                keyword in clinical_notes
                for keyword in [
                    "conservative",
                    "physical therapy",
                    "physiotherapy",
                    "medication",
                    "treatment",
                    "therapy"
                ]
            ):
                warnings.append(
                    "Conservative treatment history "
                    "may not be documented."
                )

            if not any(
                keyword in clinical_notes
                for keyword in [
                    "reason",
                    "evaluation",
                    "indicated",
                    "requested",
                    "clinical"
                ]
            ):
                warnings.append(
                    "Clinical reason for the procedure "
                    "may not be documented."
                )

        # -------------------------
        # Payer rules
        # -------------------------

        if not payer_rules:
            warnings.append(
                "No payer rules were retrieved."
            )

        # -------------------------
        # Final status
        # -------------------------

        if errors:
            status = "INVALID"
        else:
            status = "VALID"

        return {
            "status": status,
            "errors": errors,
            "warnings": warnings,
        }