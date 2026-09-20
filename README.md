# AI-Powered Prior Authorization System

An AI-powered multi-agent system that automates the prior authorization workflow by extracting information from medical documents, retrieving payer rules, validating authorization requirements, simulating submission, and tracking authorization status.

> **Project Status:** Functional prototype
> **Domain:** Healthcare AI / Intelligent Automation
> **Backend:** FastAPI
> **Frontend:** Streamlit
> **AI:** Google Gemini
> **RAG:** ChromaDB + Sentence Transformers

---

## 🚀 Overview

Prior authorization is a time-consuming healthcare administrative process that requires collecting clinical information, checking payer-specific requirements, validating documentation, submitting authorization requests, and tracking their status.

This project demonstrates how a **multi-agent AI architecture** can automate these steps through specialized agents coordinated by a central orchestrator.

The system accepts a medical document such as a PDF, image, or text file and processes it through an end-to-end authorization pipeline.

### Core Pipeline

```text
Medical Document
       ↓
Document Agent
       ↓
Extraction Agent
       ↓
RAG Agent
       ↓
Validation Agent
       ↓
Submission Agent
       ↓
Tracking Agent
       ↓
Authorization Status
```

---

## ✨ Key Features

### 📄 1. Document Processing

Supports:

* PDF documents
* PNG/JPG/JPEG images
* Text files
* Embedded PDF text extraction
* OCR fallback for scanned documents

Technologies:

* PyMuPDF
* Tesseract OCR
* Pillow

---

### 🤖 2. AI-Based Information Extraction

The Extraction Agent uses **Google Gemini** to convert unstructured clinical documents into structured authorization data.

It extracts:

* Patient information
* Date of birth
* Provider information
* Procedure
* Diagnosis
* Payer
* Clinical notes

The extracted information is validated using Pydantic schemas.

---

### 🔎 3. Retrieval-Augmented Generation

The RAG component retrieves relevant payer rules from a local vector database.

Current prototype stack:

* ChromaDB
* Sentence Transformers
* `all-MiniLM-L6-v2`

Example:

```text
Query:
ABC Health MRI Lumbar Spine prior authorization requirements

        ↓

Vector Search

        ↓

Relevant payer policy

        ↓

Validation Agent
```

This architecture allows payer-specific rules to be retrieved dynamically rather than hard-coded entirely into the validation workflow.

---

### ✅ 4. Authorization Validation

The Validation Agent combines:

* Extracted authorization information
* Retrieved payer rules
* Custom rule-engine logic

It checks for required information and supporting clinical documentation.

The validation result contains:

```json
{
  "status": "VALID",
  "errors": [],
  "warnings": []
}
```

Warnings can identify potentially missing documentation without necessarily preventing submission.

---

### 📤 5. Submission Agent

The Submission Agent currently **simulates** payer submission.

For a valid request, it generates an authorization ID such as:

```text
AUTH-6D20AC60
```

Example response:

```json
{
  "status": "SUBMITTED",
  "submission_id": "AUTH-6D20AC60",
  "message": "Authorization submitted successfully."
}
```

No real payer portal or payer API is accessed in this prototype.

---

### 📊 6. Authorization Tracking

The Tracking Agent maintains authorization status using SQLite.

Supported statuses include:

```text
SUBMITTED
PENDING
APPROVED
DENIED
```

Example:

```text
Authorization ID: AUTH-D6452CFB

Current Status: APPROVED
```

---

## 🧠 Multi-Agent Architecture

The system consists of six specialized agents coordinated by an Orchestrator.

| Agent            | Responsibility                                               |
| ---------------- | ------------------------------------------------------------ |
| Document Agent   | Extract text from uploaded documents                         |
| Extraction Agent | Convert unstructured text into structured authorization data |
| RAG Agent        | Retrieve relevant payer policies                             |
| Validation Agent | Validate authorization against payer requirements            |
| Submission Agent | Simulate authorization submission                            |
| Tracking Agent   | Store and retrieve authorization status                      |

### Orchestrator

The Orchestrator controls the complete workflow:

```text
Upload
  ↓
Document Processing
  ↓
Information Extraction
  ↓
Payer Rule Retrieval
  ↓
Validation
  ↓
Submission
  ↓
Tracking
```

It also records the processing stage and agent activity so that the frontend can display the workflow.

---

## 🏗️ System Architecture

```text
                     ┌──────────────────────┐
                     │  Streamlit Frontend  │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │    FastAPI Backend   │
                     └──────────┬───────────┘
                                │
                         Orchestrator
                                │
          ┌─────────┬───────────┼───────────┬──────────┐
          ▼         ▼           ▼           ▼          ▼
       Document  Extraction    RAG      Validation Submission
        Agent      Agent      Agent       Agent      Agent
          │          │          │           │          │
          │          ▼          ▼           │          ▼
          │       Gemini    ChromaDB        │       SQLite
          │                    │            │
          ▼                    ▼            ▼
       PyMuPDF              Payer Rules   Rule Engine
       Tesseract
```

---

## 🛠️ Technology Stack

### Backend

* Python 3.12
* FastAPI
* Uvicorn
* Pydantic

### AI / NLP

* Google Gemini
* Google GenAI SDK
* Sentence Transformers

### RAG

* ChromaDB
* `all-MiniLM-L6-v2`

### Document Processing

* PyMuPDF
* Tesseract OCR
* Pillow

### Database

* SQLite

### Frontend

* Streamlit

### Deployment / Infrastructure

* Docker
* Docker Compose
* GitHub

---

## 📁 Project Structure

```text
prior-auth-agent/
│
├── app/
│   ├── agents/
│   │   ├── document_agent.py
│   │   ├── extraction_agent.py
│   │   ├── rag_agent.py
│   │   ├── submission_agent.py
│   │   ├── tracking_agent.py
│   │   └── validation_agent.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── orchestrator/
│   │   └── orchestrator.py
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   └── retriever.py
│   │
│   ├── rules/
│   │   ├── payer_rules/
│   │   │   └── abc_health.txt
│   │   └── rule_engine.py
│   │
│   ├── schemas/
│   │   └── authorization.py
│   │
│   ├── utils/
│   │   ├── logging.py
│   │   └── ocr.py
│   │
│   └── main.py
│
├── frontend/
│   └── streamlit_app.py
│
├── documents/
│   └── input/
│
├── Dockerfile
├── Dockerfile.streamlit
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Jaswanth-3242/prior-auth-agent.git
cd prior-auth-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit `.env` to GitHub.

---

## 🧠 Initialize the RAG Database

Run:

```bash
python3 -m app.rag.ingest
```

This creates the local ChromaDB vector store containing the payer rules.

---

## ▶️ Run the Backend

Start FastAPI:

```bash
python3 -m uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

## 🖥️ Run the Frontend

In another terminal:

```bash
source venv/bin/activate
streamlit run frontend/streamlit_app.py
```

The Streamlit application will normally be available at:

```text
http://localhost:8501
```

The frontend uses the `API_URL` environment variable to locate the backend.

Example:

```bash
export API_URL=http://127.0.0.1:8000
```

---

## 🐳 Run with Docker

### Build the backend

```bash
docker build -t prior-auth-api .
```

### Run the backend

```bash
docker run --rm \
  -p 8000:8000 \
  --env-file .env \
  prior-auth-api
```

### Streamlit

The project also contains:

```text
Dockerfile.streamlit
```

for containerizing the frontend.

Docker Compose configuration is included in:

```text
docker-compose.yml
```

---

## 🔌 API Endpoints

### Health Check

```http
GET /health
```

Used to verify that the backend is running.

---

### Process Authorization

```http
POST /api/authorizations
```

Accepts an authorization document and sends it through the complete multi-agent pipeline.

The response contains:

* Document extraction
* Structured authorization information
* Retrieved/validated rules
* Validation result
* Submission result
* Tracking information
* Agent activity

---

### Track Authorization

```http
GET /api/authorizations/{submission_id}
```

Example:

```text
GET /api/authorizations/AUTH-0A981D8A
```

Returns the current authorization status.

---

## 🧪 Example Workflow

A sample request can contain:

```text
Patient: John Smith
Date of Birth: 12/04/1980

Provider: Dr. Robert Williams

Procedure: MRI Lumbar Spine

Diagnosis: Low back pain

Payer: ABC Health

Clinical Notes:
Patient reports persistent lower back pain.
MRI lumbar spine has been requested for further evaluation.
```

The system processes the request:

```text
Document
   ↓
Extract Patient / Provider / Procedure / Diagnosis / Payer
   ↓
Retrieve ABC Health rules
   ↓
Validate documentation
   ↓
Generate authorization ID
   ↓
Track status
```

Example:

```text
AUTH-6D20AC60
Status: SUBMITTED
```

---

## 🔐 Security Considerations

This project is an academic/prototype implementation.

The repository intentionally excludes:

```text
.env
venv/
authorizations.db
chroma_db/
__pycache__/
```

API credentials should be stored using environment variables rather than source code.

For a production healthcare system, additional controls would be required, including:

* Authentication and authorization
* Encryption in transit and at rest
* Secure secrets management
* Audit logging
* PHI protection
* Access controls
* Data retention policies
* Secure database infrastructure
* Production-grade monitoring
* Compliance review

---

## ⚠️ Current Prototype Limitations

### Synthetic payer rules

The current payer policy is a local synthetic rule set:

```text
ABC Health
```

It is included for demonstration purposes and does not represent an actual payer policy.

### Simulated submission

The Submission Agent generates an authorization ID locally.

It does **not** submit requests to a real insurance company or payer portal.

### Local storage

SQLite and ChromaDB are currently used for the prototype.

A production system would use managed persistent infrastructure.

### Healthcare compliance

This prototype should not be used with real patient information or for actual clinical/insurance decisions.

---

## 🚀 Deployment Architecture

The intended demonstration deployment is:

```text
                    GitHub
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
        FastAPI Backend   Streamlit Frontend
           Render          Streamlit Cloud
              │                 │
              └─────── API ─────┘
                       │
                       ▼
                  Gemini API
```

The backend is containerized using Docker, while the Streamlit frontend communicates with the deployed FastAPI API.

---

## 🔮 Future Enhancements

Potential extensions include:

* Integration with real payer APIs
* Automated payer policy ingestion
* More sophisticated clinical rule validation
* Additional payer-specific rule sets
* Human-in-the-loop review
* Authentication and role-based access control
* Production PostgreSQL database
* Persistent vector database
* Authorization analytics dashboard
* Email/SMS notifications
* Advanced document classification
* Explainable validation decisions
* Automated denial-risk detection
* Production monitoring and audit trails

---

## 📌 Project Highlights

This project demonstrates:

* Multi-agent AI architecture
* LLM-based information extraction
* Retrieval-Augmented Generation
* Vector databases
* Rule-based validation
* OCR and document processing
* REST API development
* Streamlit application development
* SQLite persistence
* Docker containerization
* Git/GitHub workflow
* End-to-end AI workflow orchestration

---

## 📄 Disclaimer

This project is an academic and technical prototype designed to demonstrate AI-driven workflow automation.

The payer rules and authorization submission workflow are simulated. The system is **not intended for real-world medical, insurance, clinical, or financial decision-making**.
