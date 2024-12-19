import os
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import json

app = FastAPI(title="Loyalty CRM Objectives Service")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LoyaltyCRMObjective(BaseModel):
    title: str
    description: str
    success_metrics: List[str]
    timeline: str
    priority: str
    required_resources: List[str]
    expected_impact: str

class PreviousData(BaseModel):
    competitor_analysis: Optional[str] = None
    customer_analysis: Optional[str] = None

class CurrentPromptData(BaseModel):
    existing_generated_output: str
    user_feedback: str

class ObjectivesRequest(BaseModel):
    company_name: str
    previous_data: Optional[PreviousData] = None
    current_prompt_data: Optional[CurrentPromptData] = None
    other_input_data: Optional[Dict] = {}

class ObjectivesResponse(BaseModel):
    generated_output: str
    structured_data: Dict

def construct_system_prompt() -> str:
    return """
You are an expert in loyalty programs and CRM strategy. Your role is to define clear, 
actionable objectives for loyalty and CRM programs based on company context, competitive 
landscape, and customer insights.

For each objective, consider:
1. Strategic alignment with business goals
2. Customer impact and value creation
3. Competitive differentiation
4. Implementation feasibility
5. Measurable success metrics

Provide your response in two parts:
1. A detailed explanation in natural language
2. A structured JSON object containing objectives with this exact schema:
{
    "loyalty_crm_objectives": [
        {
            "title": "Objective Title",
            "description": "Detailed explanation",
            "success_metrics": ["metric1", "metric2"],
            "timeline": "Q1 2024",
            "priority": "High/Medium/Low",
            "required_resources": ["resource1", "resource2"],
            "expected_impact": "Description of expected outcomes"
        }
    ]
}

Separate the two parts with [JSON_START] and [JSON_END] markers.
"""

def construct_user_prompt(
    company_name: str,
    competitor_analysis: Optional[str] = None,
    customer_analysis: Optional[str] = None,
    existing_output: Optional[str] = None,
    feedback: Optional[str] = None
) -> str:
    prompt = f"Please define loyalty and CRM objectives for {company_name}."
    
    if competitor_analysis:
        prompt += f"\n\nConsider this competitor analysis context: {competitor_analysis}"
    
    if customer_analysis:
        prompt += f"\n\nAnd this customer analysis: {customer_analysis}"
    
    if existing_output and feedback:
        prompt += f"""
\n\nPrevious objectives: {existing_output}
\nPlease refine the objectives based on this feedback: {feedback}
"""
    
    return prompt

def extract_json_from_text(text: str) -> dict:
    try:
        start_marker = "[JSON_START]"
        end_marker = "[JSON_END]"
        json_str = text[text.find(start_marker) + len(start_marker):text.find(end_marker)].strip()
        return json.loads(json_str)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse structured data from response: {str(e)}"
        )

def generate_objectives(
    company_name: str,
    competitor_analysis: Optional[str] = None,
    customer_analysis: Optional[str] = None,
    existing_output: Optional[str] = None,
    feedback: Optional[str] = None
) -> tuple[str, dict]:
    """Generate loyalty and CRM objectives using OpenAI's API"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": construct_system_prompt()},
                {"role": "user", "content": construct_user_prompt(
                    company_name,
                    competitor_analysis,
                    customer_analysis,
                    existing_output,
                    feedback
                )}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        full_response = response.choices[0].message.content
        analysis = full_response[:full_response.find("[JSON_START]")].strip()
        structured_data = extract_json_from_text(full_response)
        
        return analysis, structured_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate", response_model=ObjectivesResponse)
async def generate_analysis(request: ObjectivesRequest):
    competitor_analysis = None
    customer_analysis = None
    if request.previous_data:
        competitor_analysis = request.previous_data.competitor_analysis
        customer_analysis = request.previous_data.customer_analysis
    
    existing_output = None
    feedback = None
    if request.current_prompt_data:
        existing_output = request.current_prompt_data.existing_generated_output
        feedback = request.current_prompt_data.user_feedback
    
    generated_text, structured_data = generate_objectives(
        request.company_name,
        competitor_analysis,
        customer_analysis,
        existing_output,
        feedback
    )
    
    return ObjectivesResponse(
        generated_output=generated_text,
        structured_data=structured_data
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)