# Loyalty CRM Objectives Service

This FastAPI service generates loyalty program and CRM objectives using OpenAI's GPT-4 model, taking into account competitor and customer analysis.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/fsilva7456/loyalty-crm-objectives.git
   cd loyalty-crm-objectives
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'  # On Windows: set OPENAI_API_KEY=your-api-key-here
   ```

## Running the Service

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

2. The service will be available at `http://localhost:8000`

## API Documentation

- API documentation is available at `http://localhost:8000/docs`
- OpenAPI specification is available at `http://localhost:8000/openapi.json`

### Generate Objectives Endpoint

`POST /generate`

Example request:
```json
{
  "company_name": "Example Corp",
  "previous_data": {
    "competitor_analysis": "Competitor analysis details...",
    "customer_analysis": "Customer analysis details..."
  },
  "current_prompt_data": {
    "existing_generated_output": "Previous objectives...",
    "user_feedback": "Focus more on digital transformation"
  },
  "other_input_data": {}
}
```

Example response:
```json
{
  "generated_output": "Loyalty and CRM Objectives...\n1. Strategic Context...\n2. Key Objectives...",
  "structured_data": {
    "loyalty_crm_objectives": [
      {
        "title": "Digital Loyalty Platform Enhancement",
        "description": "Modernize the loyalty platform...",
        "success_metrics": [
          "80% digital engagement rate",
          "50% increase in mobile app usage"
        ],
        "timeline": "Q2 2024",
        "priority": "High",
        "required_resources": [
          "Development team",
          "UX designers"
        ],
        "expected_impact": "Improved customer engagement and retention"
      }
    ]
  }
}
```

## Key Features

- Uses OpenAI's GPT-4 model for generating objectives
- Incorporates competitor and customer analysis context
- Supports iterative refinement through feedback
- Provides both narrative explanation and structured objectives
- Includes success metrics and implementation details

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)