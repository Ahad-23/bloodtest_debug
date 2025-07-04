# 🐛 Bugs & Solutions

Complete debugging journey for CrewAI + FastAPI blood test analyzer project.

## 🔍 Initial Research & Setup

**Resources Used:**
- [CrewAI Tutorial](https://youtu.be/UV81LAb32g?si=5Ax41Jv1RDqSqaWk) (30 min)
- [CrewAI Documentation](https://docs.crewai.com/en/introduction)

**Initial Code Issues Found:**
- `agents.py`: No LLM defined, vague descriptions
- `task.py`: Unclear task descriptions and outputs
- `tools.py`: Missing PDFLoader, multiple TODOs

---

## 🔧 Bug Fixes

### Bug #1: Dependency Conflict
**Problem:** `crewai==0.130.0` requires `onnxruntime==1.22.0` but requirements.txt had `onnxruntime==1.18.0`

**Fix:**
```bash
# Remove pinned versions, let pip resolve
pip install -r requirements.txt
```

### Bug #2: Agent Import Error
**Error:**
```python
from crewai.agents import Agent
# ImportError: cannot import name 'Agent' from 'crewai.agents'
```

**Fix:**
```python
# ❌ Old
from crewai.agents import Agent

# ✅ New
from crewai import Agent
```

### Bug #3: Serper Tool Import
**Fix:**
```python
# ❌ Old
from crewai_tools.tools.serper_dev_tool import SerperDevTool

# ✅ New
from crewai_tools import SerperDevTool
```

### Bug #4: Missing Environment Variables
**Problem:** No `.env` file for API keys

**Fix:**
```bash
# Create .env file
touch .env
```

```ini
GEMINI_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### Bug #5: BaseTool Validation Error
**Error:**
```python
ValidationError: 1 validation error for Task
tools.0
Input should be a valid dictionary or instance of BaseTool
[type=model_type, input_value=<function BloodTestReportTool.read_data_tool>]
```

**Problem:** Tools were functions, not BaseTool classes

**Fix:**
```python
# ❌ Old
class BloodTestReportTool():
    async def read_data_tool(path='data/sample.pdf'):
        ...

# ✅ New
from crewai import BaseTool
from langchain_community.document_loaders import PyPDFLoader

class BloodTestReportTool(BaseTool):
    name = "Blood Test Report Reader"
    description = "Reads blood test PDF and extracts text"
    
    def _run(self, file_path='data/sample.pdf'):
        docs = PyPDFLoader(file_path=file_path).load()
        full_report = ""
        for doc in docs:
            content = doc.page_content.replace("\n\n", "\n")
            full_report += content + "\n"
        return full_report
```

**Usage:**
```python
# ❌ Old
tools=[BloodTestReportTool().read_data_tool]

# ✅ New
tools=[BloodTestReportTool()]
```

### Bug #6: Missing FastAPI Dependency
**Error:**
```python
RuntimeError: Form data requires "python-multipart" to be installed.
```

**Fix:**
```bash
pip install python-multipart
```

### Bug #7: Pydantic Deprecation Warning
**Warning:**
```python
PydanticDeprecatedSince20: Using extra keyword arguments on Field is deprecated
```

**Fix:**
```python
# ❌ Old
Field(..., required=True)

# ✅ New
Field(..., json_schema_extra={"required": True})
```

### Bug #8: PDFLoader Import
**Fix:**
```python
from langchain_community.document_loaders import PyPDFLoader as PDFLoader
```

### Bug #9: LLM Configuration
**Fix:**
```python
from crewai import LLM

llm = LLM(model="gemini/gemini-1.5-flash")

agent = Agent(
    role="Blood Test Analyst",
    goal="Analyze blood test reports",
    backstory="Expert in medical data analysis",
    llm=llm,
    tools=[BloodTestReportTool()]
)
```

---

## 📝 Key Learnings

1. **Check documentation first** - import syntax changes between versions
2. **Use virtual environments** - isolate dependencies
3. **Let pip resolve dependencies** - avoid hard-pinning when possible
4. **BaseTool requires `_run()` method** - not async functions
5. **FastAPI file uploads need `python-multipart`**
6. **Environment variables are crucial** - create `.env` files
7. **Pydantic v2 syntax differs** - use `json_schema_extra`



## 🚀 Final Status

✅ **Working Components:**
- CrewAI agents with proper LLM configuration
- Custom BaseTool implementations
- FastAPI endpoints with file upload support
- Environment variable management
- All dependencies resolved and compatible

**Final Result:** Fully functional blood test analyzer