from ..base_skill import BaseSkill
from ..skill_loader import register_skill
from aj_mas.utils import logger
import random

@register_skill
class SymptomCheckerSkill(BaseSkill):
    def __init__(self):
        super().__init__("SymptomCheckerSkill", "Check symptoms and provide health advice")

    def execute(self, parameters: dict) -> dict:
        symptoms = parameters.get('symptoms', [])
        age = parameters.get('age')
        gender = parameters.get('gender')

        logger.log(f"Checking symptoms for {age}-year-old {gender}: {', '.join(symptoms)}")
        
        diagnosis = self._analyze_symptoms(symptoms, age, gender)

        result = {"diagnosis": diagnosis}
        self.log_execution(parameters, result)
        return result

    def _analyze_symptoms(self, symptoms, age, gender):
        # In a real implementation, this would use a medical knowledge base and more sophisticated analysis
        possible_conditions = ["Common Cold", "Flu", "Allergies", "Stress", "Dehydration"]
        severity = random.choice(["Mild", "Moderate", "Severe"])
        
        recommendations = [
            "Rest and stay hydrated",
            "Take over-the-counter pain relievers if needed",
            "Monitor your symptoms"
        ]
        
        if severity == "Severe" or len(symptoms) > 3:
            recommendations.append("Consult a healthcare professional")

        return {
            "possible_conditions": random.sample(possible_conditions, k=min(len(possible_conditions), len(symptoms))),
            "severity": severity,
            "recommendations": recommendations,
            "disclaimer": "This is not a professional medical diagnosis. Please consult a doctor for accurate medical advice."
        }