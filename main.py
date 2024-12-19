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