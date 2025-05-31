import joblib
import json
from pathlib import Path
from typing import Dict, Any
import logging

class DisasterModelLoader:
    def __init__(self, models_dir="../models"):
        self.models_dir = Path(models_dir)
        self.emergency_model = None
        self.urgency_model = None
        self.logger = logging.getLogger(__name__)
    
    def load_models(self):
        try:
            emergency_path = self.models_dir / "emergency_classifier.zip"
            if emergency_path.exists():
                self.emergency_model = joblib.load(emergency_path)
                self.logger.info(f"Emergency classifier loaded")
            
            urgency_path = self.models_dir / "urgency_classifier.zip"
            if urgency_path.exists():
                self.urgency_model = joblib.load(urgency_path)
                self.logger.info(f"Urgency classifier loaded")
            
            return self.emergency_model is not None and self.urgency_model is not None
        except Exception as e:
            self.logger.error(f"Error loading models: {str(e)}")
            return False
    
    def classify_emergency(self, text):
        if self.emergency_model is None:
            return {"error": "Emergency model not loaded"}
        try:
            prediction = self.emergency_model.predict([text])[0]
            probability = self.emergency_model.predict_proba([text])[0]
            return {
                "is_emergency": bool(prediction),
                "confidence": float(max(probability)),
                "probabilities": {
                    "emergency": float(probability[1]) if len(probability) > 1 else float(probability[0]),
                    "non_emergency": float(probability[0]) if len(probability) > 1 else 1 - float(probability[0])
                }
            }
        except Exception as e:
            return {"error": f"Classification failed: {str(e)}"}
    
    def classify_urgency(self, text):
        if self.urgency_model is None:
            return {"error": "Urgency model not loaded"}
        try:
            prediction = self.urgency_model.predict([text])[0]
            probability = self.urgency_model.predict_proba([text])[0]
            urgency_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
            return {
                "urgency_level": urgency_levels[prediction] if prediction < len(urgency_levels) else "UNKNOWN",
                "confidence": float(max(probability)),
                "probabilities": {
                    level: float(prob) for level, prob in zip(urgency_levels, probability)
                }
            }
        except Exception as e:
            return {"error": f"Urgency classification failed: {str(e)}"}
    
    def analyze_request(self, text):
        emergency_result = self.classify_emergency(text)
        if emergency_result.get("is_emergency", False):
            urgency_result = self.classify_urgency(text)
            return {
                "text": text,
                "emergency_analysis": emergency_result,
                "urgency_analysis": urgency_result,
                "requires_immediate_action": urgency_result.get("urgency_level") in ["HIGH", "CRITICAL"]
            }
        else:
            return {
                "text": text,
                "emergency_analysis": emergency_result,
                "urgency_analysis": {"urgency_level": "N/A", "message": "Not classified as emergency"},
                "requires_immediate_action": False
            }
