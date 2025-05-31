# Disaster Response AI Models

## Setup
1. cd disaster_response_models
2. python -m venv venv
3. venv\Scripts\activate
4. pip install -r requirements.txt
5. Add your models to models/ folder:
   - emergency_classifier.zip
   - urgency_classifier.zip

## Test
cd integration
python test_models.py

## Run API
cd integration
python api_integration.py
