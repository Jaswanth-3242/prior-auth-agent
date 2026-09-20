from datetime import datetime

from app.database.database import (
    get_connection,
    initialize_database,
)


class TrackingAgent:

    def __init__(self):
        initialize_database()

    def create_record(self, submission_result):

        if submission_result["status"] != "SUBMITTED":
            return {
                "status": "NOT_TRACKED",
                "message": "Submission was not successful."
            }

        now = datetime.now().isoformat()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO authorizations (
                submission_id,
                patient_name,
                payer,
                procedure,
                status,
                submitted_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                submission_result["submission_id"],
                submission_result["patient"],
                submission_result["payer"],
                submission_result["procedure"],
                "SUBMITTED",
                submission_result["submitted_at"],
                now,
            ),
        )

        connection.commit()
        connection.close()

        return {
            "status": "TRACKING",
            "submission_id": submission_result["submission_id"],
            "current_status": "SUBMITTED",
            "updated_at": now,
        }

    def update_status(
        self,
        submission_id: str,
        new_status: str
    ):

        allowed_statuses = {
            "SUBMITTED",
            "PENDING",
            "APPROVED",
            "DENIED",
        }

        if new_status not in allowed_statuses:
            raise ValueError(
                f"Invalid status: {new_status}"
            )

        now = datetime.now().isoformat()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE authorizations
            SET status = ?, updated_at = ?
            WHERE submission_id = ?
            """,
            (
                new_status,
                now,
                submission_id,
            ),
        )

        connection.commit()

        updated_rows = cursor.rowcount

        connection.close()

        if updated_rows == 0:
            return {
                "status": "NOT_FOUND",
                "submission_id": submission_id,
            }

        return {
            "status": "UPDATED",
            "submission_id": submission_id,
            "current_status": new_status,
            "updated_at": now,
        }

    def get_status(self, submission_id: str):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                submission_id,
                patient_name,
                payer,
                procedure,
                status,
                submitted_at,
                updated_at
            FROM authorizations
            WHERE submission_id = ?
            """,
            (submission_id,),
        )

        row = cursor.fetchone()

        connection.close()

        if not row:
            return {
                "status": "NOT_FOUND",
                "submission_id": submission_id,
            }

        return {
            "submission_id": row[0],
            "patient_name": row[1],
            "payer": row[2],
            "procedure": row[3],
            "current_status": row[4],
            "submitted_at": row[5],
            "updated_at": row[6],
        }