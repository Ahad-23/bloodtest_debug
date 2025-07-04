# Blood Test Report Analyser 🩺

A medical assistant powered by AI agents that can read a user's uploaded blood test PDF, verify its structure, extract medical biomarkers, and return evidence-based nutrition and exercise recommendations using domain-specialized agents.

---

## 🧠 Project Overview

This project leverages [CrewAI](https://docs.crewai.com/) agents to simulate a real-world team of medical specialists working together on a blood test report:
- **Verifier Agent**: Validates the uploaded PDF.
- **Doctor Agent**: Analyzes the report and interprets biomarkers.
- **Nutritionist Agent**: Recommends diet based on report insights.
- **Exercise Specialist**: Suggests exercise plans aligned with medical condition.

All orchestrated via [FastAPI](https://fastapi.tiangolo.com/) for a clean, modern API-based backend.

---

## 🛠️ Tech Stack

| Area               | Tools / Libraries                             |
|--------------------|-----------------------------------------------|
| Backend            | Python, FastAPI                               |
| Agents Framework   | CrewAI                                        |
| PDF Parsing        | langchain-community PyPDFLoader               |
| Search Tool        | SerperDevTool                                 |
| AI Models          | Gemini 1.5 Flash (via CrewAI LLM wrapper)     |
| Others             | python-multipart, pydantic, dotenv, uvicorn   |

---

## ✅ Features

- Upload PDF blood test report
- Verify if report is a valid medical test
- Parse out values like Hemoglobin, WBC, Glucose, etc.
- Get personalized:
  - Medical summary
  - Nutrition plan
  - Exercise plan
- Built with domain-aware CrewAI agents
- Clean JSON API responses

---

## 📦 Setup Instructions

### 1. Clone and Setup

```bash
git clone <https://github.com/Ahad-23/bloodtest_debug.git>
cd bloodtest_debug

# (Recommended) Setup virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Environment Variables

Create a `.env` file in the root:

```
SERPER_API_KEY=<your_serper_api_key>
GEMINI_API_KEY=<your_gemini_api_key>
```

> Ensure your `tools.py` and `agents.py` use `LLM(model="gemini/gemini-2.0-flash")` under the hood.

---

### 3. Run the Server

```bash
uvicorn main:app --reload
```

Server will be live at:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🚀 API Endpoints

### `GET /`
Health check for the API.

### `POST /analyze`
Run full agent pipeline (verification + doctor + nutrition + exercise)

#### Request

- **Content-Type**: `multipart/form-data`
- **Params**:
  - `file`: Blood test PDF
  - `query`: (optional) A custom query like "Summarise my blood test"

#### Response

```json
{
  "status": "success",
  "query": "...",
  "file_processed": "blood_test.pdf",
  "analysis": {
    "summary": "...",
    "detailed_reports": {
      "verification_report": "...",
      "medical_analysis": "...",
      "nutrition_recommendations": "...",
      "exercise_recommendations": "..."
    }
  }
}
```


---

## 🐞 Bugs Fixed (Approach)

> Full details in [`BUGS.md`](BUGS.md), but a summary:

| Bug | Root Cause | Fix |
|-----|------------|-----|
| `BaseTool` ImportError | Incorrect tool structure and import | Switched to new `tool` decorator or `BaseTool` class with proper schemas |
| Agent tool errors | Tools were passed as async functions | Refactored all tools as `BaseTool` subclasses |
| `verbose` keyword duplicated | Passed manually & via `**kwargs` | Removed duplicate verbose param |
| Gemini model failed | `Crew` expected OpenAI key by default | Passed Gemini model correctly via CrewAI’s LLM wrapper |
| Swagger UI broken | Missing JS bundle or invalid certificate | Used a REST client (Postman or curl) instead |
| requirements bloated | Accidentally pushed `.venv` | Cleaned `.gitignore`, regenerated `requirements.txt` with `pipreqs` |
| `python-multipart` missing | Required for file upload | Installed explicitly |
| `git restore .` failed | Repo not initialized or clean | Ran `git init`, `.gitignore`, and re-committed properly |

---

## 📁 Folder Structure

```
├── agents.py               # Defines all 4 agents with domain-specific goals and tools
├── tools.py                # All tools wrapped as CrewAI BaseTool classes
├── main.py                 # FastAPI server logic
├── test_upload.py          # Script to test file upload endpoint
├── data/                   # Upload destination for PDFs
├── outputs/                # Logs and agent markdown outputs
├── .env                    # Serper/Gemini keys (excluded from repo)
├── requirements.txt        # Cleaned up Python requirements
└── README.md
```

---

## 🧪 Local Testing

```bash
python test_upload.py
```

> Uploads a local `sample.pdf` to `POST /analyze` and prints results.


---

## 🔒 Disclaimer

This system is for **educational/demo purposes** and **not a medical diagnostic tool**.  
Always consult certified health professionals before acting on medical data.