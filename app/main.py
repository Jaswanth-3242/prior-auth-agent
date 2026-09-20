from pathlib import Path
import shutil
import uuid

from fastapi import FastAPI, File, UploadFile, HTTPException

from app.orchestrator.orchestrator import Orchestrator


app = FastAPI(
    title="Prior Authorization AI",
    description="AI-powered prior authorization processing system",
    version="1.0.0",
)


orchestrator = Orchestrator()


INPUT_DIRECTORY = Path("documents/input")
INPUT_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Prior Authorization AI",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api/authorizations")
async def process_authorization(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    extension = Path(file.filename).suffix.lower()

    allowed_extensions = {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
        ".txt",
    }

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}"
        )

    unique_filename = (
        f"{uuid.uuid4().hex}{extension}"
    )

    file_path = INPUT_DIRECTORY / unique_filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        result = orchestrator.process(
            str(file_path)
        )

        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
@app.get("/api/authorizations/{submission_id}")
def get_authorization_status(submission_id: str):
    result = orchestrator.tracking_agent.get_status(submission_id)

    if result.get("status") == "NOT_FOUND":
        raise HTTPException(status_code=404, detail="Authorization not found.")

    return result