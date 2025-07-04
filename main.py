from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

from crewai import Crew, Process
from agents import doctor, verifier, nutritionist, exercise_specialist
from task import verification_task, medical_analysis_task, nutrition_task, exercise_task

app = FastAPI(title="Blood Test Report Analyser")

def run_crew(query: str, file_path: str = "data/sample.pdf"):
    medical_crew = Crew(
        agents=[verifier, doctor, nutritionist, exercise_specialist],
        tasks=[verification_task, medical_analysis_task, nutrition_task, exercise_task],
        process=Process.sequential,
        verbose=True,
        memory=True,
        output_log_file="outputs/crew_log.txt"
    )
    result = medical_crew.kickoff(inputs={
        'query': query,
        'file_path': file_path
    })
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        # Ensure data and outputs directories exist
        os.makedirs("data", exist_ok=True)
        os.makedirs("outputs", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if query == "" or query is None:
            query = "Summarise my Blood Test Report"
            
        # Process the blood report with all specialists
        response=run_crew(query=query.strip(),file_path=file_path)
        
        # FIXED: Read the generated output files for structured response
        output_files = {}
        output_dir = "outputs"
        
        # Try to read generated output files
        output_file_names = [
            "verification_report.md",
            "medical_analysis.md", 
            "nutrition_recommendations.md",
            "exercise_recommendations.md"
        ]
        
        for filename in output_file_names:
            file_full_path = os.path.join(output_dir, filename)
            if os.path.exists(file_full_path):
                try:
                    with open(file_full_path, 'r', encoding='utf-8') as f:
                        output_files[filename.replace('.md', '')] = f.read()
                except Exception as e:
                    output_files[filename.replace('.md', '')] = f"Error reading {filename}: {str(e)}"
        
        return {
            "status": "success",
            "query": query,
            "file_processed": file.filename,
            "analysis": {
                "summary": str(response),
                "detailed_reports": output_files
            },
            "reports_generated": list(output_files.keys())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass



if __name__ == "__main__":
    import uvicorn
    print("Starting Blood Test Report Analyser API...")
    print("Available endpoints:")
    print("   - GET  /         : Health check")
    print("   - POST /analyze  : Full analysis with all specialists")
    print("🚀 Server starting on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)