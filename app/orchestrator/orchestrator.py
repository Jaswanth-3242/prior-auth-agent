from datetime import datetime

from app.agents.document_agent import DocumentAgent
from app.agents.extraction_agent import ExtractionAgent
from app.rag.retriever import RAGRetriever
from app.agents.validation_agent import ValidationAgent
from app.agents.submission_agent import SubmissionAgent
from app.agents.tracking_agent import TrackingAgent


class Orchestrator:

    def __init__(self):
        self.document_agent = DocumentAgent()
        self.extraction_agent = ExtractionAgent()
        self.rag_retriever = RAGRetriever()
        self.validation_agent = ValidationAgent()
        self.submission_agent = SubmissionAgent()
        self.tracking_agent = TrackingAgent()

    def _agent_status(
        self,
        name: str,
        status: str,
        message: str
    ):
        return {
            "agent": name,
            "status": status,
            "message": message,
        }

    def _failure(
        self,
        stage: str,
        error: Exception,
        started_at: str,
        agent_activity=None
    ):
        return {
            "status": "FAILED",
            "stage": stage,
            "error": str(error),
            "agent_activity": agent_activity or [],
            "started_at": started_at,
            "completed_at": datetime.now().isoformat(),
        }

    def process(self, file_path: str):

        started_at = datetime.now().isoformat()

        # Stores the status of every agent
        agent_activity = []

        # -------------------------
        # 1. Document processing
        # -------------------------

        try:
            document = self.document_agent.process(
                file_path
            )

            agent_activity.append(
                self._agent_status(
                    "Document Agent",
                    "COMPLETED",
                    "Document text extracted successfully."
                )
            )

        except Exception as error:
            return self._failure(
                "DOCUMENT",
                error,
                started_at,
                agent_activity
            )

        # -------------------------
        # 2. Data extraction
        # -------------------------

        try:
            authorization = self.extraction_agent.extract(
                document["text"]
            )

            agent_activity.append(
                self._agent_status(
                    "Extraction Agent",
                    "COMPLETED",
                    "Structured authorization data extracted."
                )
            )

        except Exception as error:
            return self._failure(
                "EXTRACTION",
                error,
                started_at,
                agent_activity
            )

        # -------------------------
        # 3. Retrieve payer rules
        # -------------------------

        try:
            query = (
                f"{authorization.payer.name} "
                f"{authorization.procedure.description} "
                f"prior authorization requirements"
            )

            retrieved_rules = self.rag_retriever.retrieve(
                query
            )

            agent_activity.append(
                self._agent_status(
                    "RAG Agent",
                    "COMPLETED",
                    f"Retrieved {len(retrieved_rules)} "
                    f"relevant payer rule(s)."
                )
            )

        except Exception as error:
            return self._failure(
                "RAG_RETRIEVAL",
                error,
                started_at,
                agent_activity
            )

        # -------------------------
        # 4. Validation
        # -------------------------

        try:
            validation = self.validation_agent.validate(
                authorization,
                retrieved_rules
            )

            agent_activity.append(
                self._agent_status(
                    "Validation Agent",
                    validation["status"],
                    (
                        f"Validation completed with "
                        f"{len(validation['errors'])} error(s) "
                        f"and "
                        f"{len(validation['warnings'])} warning(s)."
                    )
                )
            )

        except Exception as error:
            return self._failure(
                "VALIDATION",
                error,
                started_at,
                agent_activity
            )

        # -------------------------
        # Stop if validation failed
        # -------------------------

        if validation["status"] != "VALID":
            return {
                "status": "VALIDATION_FAILED",
                "stage": "VALIDATION",
                "document": document,
                "authorization": authorization,
                "validation": validation,
                "submission": None,
                "tracking": None,
                "agent_activity": agent_activity,
                "started_at": started_at,
                "completed_at": datetime.now().isoformat(),
            }

        # -------------------------
        # 5. Submission
        # -------------------------

        try:
            submission = self.submission_agent.submit(
                authorization,
                validation
            )

            agent_activity.append(
                self._agent_status(
                    "Submission Agent",
                    submission["status"],
                    submission["message"]
                )
            )

        except Exception as error:
            return self._failure(
                "SUBMISSION",
                error,
                started_at,
                agent_activity
            )

        # -------------------------
        # Stop if submission failed
        # -------------------------

        if submission["status"] != "SUBMITTED":
            return {
                "status": "SUBMISSION_FAILED",
                "stage": "SUBMISSION",
                "document": document,
                "authorization": authorization,
                "validation": validation,
                "submission": submission,
                "tracking": None,
                "agent_activity": agent_activity,
                "started_at": started_at,
                "completed_at": datetime.now().isoformat(),
            }

        # -------------------------
        # 6. Tracking
        # -------------------------

        try:
            tracking = self.tracking_agent.create_record(
                submission
            )

            agent_activity.append(
                self._agent_status(
                    "Tracking Agent",
                    "COMPLETED",
                    "Authorization added to tracking database."
                )
            )

        except Exception as error:
            return self._failure(
                "TRACKING",
                error,
                started_at,
                agent_activity
            )

        # -------------------------
        # Final result
        # -------------------------

        return {
            "status": "SUCCESS",
            "stage": "COMPLETE",
            "document": document,
            "authorization": authorization,
            "validation": validation,
            "submission": submission,
            "tracking": tracking,
            "agent_activity": agent_activity,
            "started_at": started_at,
            "completed_at": datetime.now().isoformat(),
        }