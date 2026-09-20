# 🤖 AI-Powered Prior Authorization System

An end-to-end **AI-powered Prior Authorization system** that automates document processing, clinical information extraction, payer-rule retrieval, validation, submission simulation, and authorization tracking.

The system uses a **multi-agent architecture** orchestrated through a FastAPI backend, with a Streamlit web interface.

## 🚀 Live Demo

**Frontend:**
https://prior-auth-agent-frontend.onrender.com

The application is deployed on Render and can be accessed directly through the link above.

---

## 🏗️ System Architecture

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │ Streamlit UI    │
                  │    Frontend     │
                  └────────┬────────┘
                           │ HTTPS
                           ▼
                  ┌─────────────────┐
                  │   FastAPI       │
                  │    Backend      │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   Orchestrator  │
                  └────────┬────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   Document    │  │  Extraction   │  │      RAG      │
│     Agent     │  │     Agent     │  │     Agent     │
└───────────────┘  └───────────────┘  └───────┬───────┘
                                              │
                                      ┌───────▼────────┐
                                      │    FastEmbed   │
                                      │   + ChromaDB   │
                                      └───────┬────────┘
                                              │
        ┌─────────────────────────────────────┘
        │
        ▼
┌───────────────┐
│  Validation   │
│     Agent     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Submission   │
│     Agent     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   Tracking    │
│     Agent     │
└───────────────┘
```

---

## 🧠 Multi-Agent Workflow

### 1. 📄 Document Agent

Processes uploaded authorization documents.

Supported formats:

* PDF
* PNG
* JPG/JPEG
* TXT

For PDFs, embedded text is extracted when available.

For scanned/image documents, **Tesseract OCR** is used to extract text.

### 2. 🔍 Extraction Agent

Uses **Google Gemini** to extract structured information from the document.

Extracted information includes:

* Patient information
* Provider information
* Procedure
* Diagnosis
* Payer
* Clinical notes

### 3. 🔎 RAG Agent

Retrieves relevant payer rules from the local knowledge base.

Technology:

* **FastEmbed**
* **ChromaDB**
* `BAAI/bge-small-en-v1.5` embedding model

The retrieved payer rules are passed to the validation stage.

### 4. ✅ Validation Agent

Validates the authorization request against:

* Required patient information
* Provider information
* Procedure information
* Diagnosis
* Clinical documentation
* Retrieved payer rules

The rule engine identifies:

* Errors
* Warnings
* Validation status

### 5. 📤 Submission Agent

Simulates submission of a validated authorization request.

A unique authorization ID is generated, for example:

```text
AUTH-XXXXXXXX
```

Invalid requests are not submitted.

### 6. 📊 Tracking Agent

Stores and tracks authorization status using SQLite.

Supported statuses include:

```text
SUBMITTED
PENDING
APPROVED
DENIED
```

Authorization records can be retrieved using their submission ID.

---

## 🛠️ Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* SQLite

### AI / NLP

* Google Gemini
* FastEmbed
* ONNX Runtime

### RAG

* ChromaDB
* `BAAI/bge-small-en-v1.5`

### Document Processing

* PyMuPDF
* Pillow
* Tesseract OCR
* pytesseract

### Frontend

* Streamlit
* Requests

### Deployment

* Docker
* Render
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
│   │   ├── validation_agent.py
│   │   ├── submission_agent.py
│   │   └── tracking_agent.py
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
│   │   └── ocr.py
│   │
│   └── main.py
│
├── frontend/
│   └── streamlit_app.py
│
├── documents/
│
├── Dockerfile
├── requirements.txt
├── runtime.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Jaswanth-3242/prior-auth-agent.git
cd prior-auth-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
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

### 5. Start the FastAPI backend

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Backend:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/health
```

### 6. Start the Streamlit frontend

In another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Frontend:

```text
http://localhost:8501
```

---

## 🐳 Docker Deployment

The backend Docker image includes the system-level **Tesseract OCR** dependency required for scanned/image documents.

Build:

```bash
docker build -t prior-auth-agent .
```

Run:

```bash
docker run --rm -p 8000:8000 --env-file .env prior-auth-agent
```

The Docker deployment is used for the production backend because it allows Tesseract OCR to be installed inside the container.

---

## 🔐 Environment Variables

The application requires:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never commit `.env` or API keys to GitHub.

---

## 📋 Example Workflow

A typical request follows this flow:

```text
Upload authorization document
          ↓
Document extraction / OCR
          ↓
Clinical information extraction
          ↓
Retrieve relevant payer rules
          ↓
Validate authorization
          ↓
Submit if valid
          ↓
Generate authorization ID
          ↓
Track authorization status
```

---

## 🎯 Current Capabilities

* ✅ PDF document processing
* ✅ Image/scanned document OCR
* ✅ Structured clinical information extraction
* ✅ Gemini-powered extraction
* ✅ RAG-based payer-rule retrieval
* ✅ FastEmbed-based embeddings
* ✅ ChromaDB vector search
* ✅ Rule-based authorization validation
* ✅ Validation warnings and errors
* ✅ Simulated authorization submission
* ✅ Authorization ID generation
* ✅ SQLite tracking
* ✅ Multi-agent orchestration
* ✅ Streamlit web interface
* ✅ FastAPI REST API
* ✅ Docker deployment
* ✅ Public Render deployment

---

## ⚠️ Prototype Limitations

This project is currently a **working prototype**.

* Payer rules currently use a synthetic/local payer rule dataset.
* Authorization submission is simulated and does not connect to real payer portals or APIs.
* Tracking uses a local SQLite database.
* Production deployment would require additional healthcare security controls.
* Real-world deployment would require appropriate handling of PHI, authentication, authorization, encryption, auditing, compliance, and secure data storage.

---

## 🔮 Future Improvements

Potential future enhancements include:

* Integration with real payer APIs
* Automated payer portal submission
* Additional payer rule databases
* More advanced clinical validation
* Human-in-the-loop review
* Authentication and role-based access control
* Production-grade database
* Audit logging
* Notification services
* Authorization status webhooks
* Improved document classification
* FHIR/HL7 integration
* Healthcare compliance and security controls

---

## 👨‍💻 Author

**Jaswanth-3242**

GitHub:
https://github.com/Jaswanth-3242
