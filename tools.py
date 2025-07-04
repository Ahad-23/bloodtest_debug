import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader as PDFLoader
from crewai_tools import SerperDevTool
from crewai.tools import BaseTool
import json
import re
from typing import Dict, List, Any

# Creating search tool
search_tool = SerperDevTool()

class BloodTestReportTool(BaseTool):
    name: str = "Blood Test Report Reader"
    description: str = "Reads a blood test PDF file and returns the extracted text content"
    
    def _run(self, file_path: str = 'data/sample.pdf') -> str:
        """Read and extract text from PDF blood test report"""
        try:
            docs = PDFLoader(file_path=file_path).load()
            full_report = ""
            for data in docs:
                content = data.page_content.replace("\n\n", "\n")
                full_report += content + "\n"
            return full_report.strip()
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"
    
    @staticmethod
    def read_data_tool(path: str = 'data/sample.pdf') -> str:
        """Static method for backward compatibility"""
        tool = BloodTestReportTool()
        return tool._run(path)

class BloodReportParserTool(BaseTool):
    name: str = "Blood Report Parser"
    description: str = "Parses blood report text and extracts structured biomarker data"
    
    def _run(self, report_text: str) -> str:
        """Parse blood report text and extract key biomarkers"""
        try:
            # Common blood test patterns
            patterns = {
                'hemoglobin': r'h[ae]moglobin.*?(\d+\.?\d*)\s*g/dl',
                'wbc': r'wbc.*?(\d+\.?\d*)',
                'rbc': r'rbc.*?(\d+\.?\d*)',
                'platelets': r'platelet.*?(\d+\.?\d*)',
                'glucose': r'glucose.*?(\d+\.?\d*)',
                'cholesterol': r'cholesterol.*?(\d+\.?\d*)',
                'creatinine': r'creatinine.*?(\d+\.?\d*)',
                'bilirubin': r'bilirubin.*?(\d+\.?\d*)'
            }
            
            extracted_values = {}
            report_lower = report_text.lower()
            
            for marker, pattern in patterns.items():
                match = re.search(pattern, report_lower)
                if match:
                    extracted_values[marker] = {
                        'value': float(match.group(1)),
                        'found_in_text': True
                    }
            
            return json.dumps(extracted_values, indent=2)
        except Exception as e:
            return f"Error parsing report: {str(e)}"

class NutritionAnalysisTool(BaseTool):
    name: str = "Nutrition Analysis Tool"
    description: str = "Analyzes blood markers and provides evidence-based nutritional recommendations"
    
    def _run(self, blood_data: str) -> str:
        """Analyze blood data for nutritional insights"""
        try:
            # Parse blood data if it's JSON
            if blood_data.startswith('{'):
                data = json.loads(blood_data)
            else:
                data = {}
            
            recommendations = {
                'dietary_recommendations': [],
                'nutrients_to_focus': [],
                'foods_to_include': [],
                'foods_to_limit': [],
                'hydration_advice': 'Maintain adequate hydration (8-10 glasses of water daily)'
            }
            
            # Add specific recommendations based on common markers
            recommendations['dietary_recommendations'].extend([
                'Follow a balanced Mediterranean-style diet rich in fruits, vegetables, whole grains, and lean proteins',
                'Include omega-3 rich foods like fatty fish, walnuts, and flaxseeds',
                'Ensure adequate fiber intake (25-35g daily) through whole foods'
            ])
            
            return json.dumps(recommendations, indent=2)
        except Exception as e:
            return f"Error in nutrition analysis: {str(e)}"

class ExercisePlanningTool(BaseTool):
    name: str = "Exercise Planning Tool"
    description: str = "Creates safe, personalized exercise recommendations based on health data"
    
    def _run(self, health_data: str) -> str:
        """Generate safe exercise recommendations"""
        try:
            exercise_plan = {
                'general_guidelines': [
                    'Consult with healthcare provider before starting any new exercise program',
                    'Start gradually and progress slowly',
                    'Listen to your body and rest when needed'
                ],
                'cardiovascular_exercise': {
                    'frequency': '150 minutes moderate intensity or 75 minutes vigorous per week',
                    'activities': ['brisk walking', 'swimming', 'cycling', 'dancing'],
                    'progression': 'Start with 10-15 minutes, gradually increase duration'
                },
                'strength_training': {
                    'frequency': '2-3 times per week',
                    'focus': 'Major muscle groups',
                    'progression': 'Start with bodyweight exercises, add resistance gradually'
                },
                'flexibility': {
                    'frequency': 'Daily',
                    'activities': ['stretching', 'yoga', 'tai chi'],
                    'duration': '10-15 minutes'
                },
                'important_notes': [
                    'Monitor heart rate if cardiovascular issues are present',
                    'Stay hydrated during exercise',
                    'Stop exercise if experiencing chest pain, dizziness, or shortness of breath'
                ]
            }
            
            return json.dumps(exercise_plan, indent=2)
        except Exception as e:
            return f"Error creating exercise plan: {str(e)}"