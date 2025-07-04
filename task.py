from crewai import Task
from tools import BloodTestReportTool,NutritionAnalysisTool,ExercisePlanningTool,BloodReportParserTool
from agents import verifier,doctor,nutritionist,exercise_specialist
# Document Verification Task
verification_task = Task(
    description=(
        "Verify the uploaded document to ensure it is a legitimate blood test report. "
        "Check for the presence of key components such as patient information, "
        "test parameters, reference ranges, and laboratory identification. "
        "Confirm the document is readable and contains sufficient data for analysis. "
        "Document path: {file_path}"
    ),
    expected_output=(
        "A verification report stating whether the document is a valid blood test report, "
        "listing what key components are present or missing, and confirming if the "
        "document is suitable for medical analysis. Include any data quality concerns."
    ),
    agent=verifier,
    tools=[BloodTestReportTool()],
    output_file="outputs/verification_report.md"
)

# Medical Analysis Task
medical_analysis_task = Task(
    description=(
        "Analyze the blood test report to identify and interpret key biomarkers. "
        "Compare results against standard reference ranges, identify any abnormal "
        "values, and explain their potential clinical significance. Provide "
        "educational information about what the results might indicate while "
        "emphasizing that this is not a medical diagnosis. "
        "User query: {query}"
    ),
    expected_output=(
        "A comprehensive medical analysis report including: "
        "1. Summary of key biomarkers and their values "
        "2. Identification of normal and abnormal results "
        "3. Clinical significance of abnormal findings "
        "4. General health insights based on the overall pattern "
        "5. Clear disclaimer about the need for professional medical consultation "
        "6. Recommendations for follow-up or further testing if indicated"
    ),
    agent=doctor,
    tools=[BloodTestReportTool(), BloodReportParserTool()],
    output_file="outputs/medical_analysis.md",
    context=[verification_task]
)

# Nutrition Analysis Task
nutrition_task = Task(
    description=(
        "Based on the blood test analysis, provide evidence-based nutritional "
        "guidance that may help support optimal health. Focus on dietary patterns, "
        "specific nutrients that may be relevant to the blood markers, and "
        "general nutritional recommendations. User query: {query}"
    ),
    expected_output=(
        "A nutritional guidance report including: "
        "1. Dietary recommendations based on blood test findings "
        "2. Specific nutrients to focus on or monitor "
        "3. Food sources rich in recommended nutrients "
        "4. General dietary patterns that support health "
        "5. Foods to limit if relevant to findings "
        "6. Disclaimer emphasizing this is nutritional guidance, not medical advice"
    ),
    agent=nutritionist,
    tools=[NutritionAnalysisTool()],
    output_file="outputs/nutrition_recommendations.md",
    context=[medical_analysis_task]
)

# Exercise Planning Task
exercise_task = Task(
    description=(
        "Create a safe, evidence-based exercise recommendation plan considering "
        "the health status indicated by the blood test results. Focus on "
        "general fitness guidelines while noting any precautions that may "
        "be relevant based on the findings. User query: {query}"
    ),
    expected_output=(
        "An exercise guidance report including: "
        "1. General exercise recommendations appropriate for the health profile "
        "2. Specific considerations based on blood test findings "
        "3. Progression guidelines starting from current fitness level "
        "4. Safety precautions and warning signs to watch for "
        "5. Types of exercise that may be most beneficial "
        "6. Strong recommendation to consult healthcare provider before starting"
    ),
    agent=exercise_specialist,
    tools=[ExercisePlanningTool()],
    output_file="outputs/exercise_recommendations.md",
    context=[medical_analysis_task]
)

