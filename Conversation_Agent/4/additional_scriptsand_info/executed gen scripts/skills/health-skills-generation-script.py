import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def create_health_skills():
    health_dir = "aj_mas/skills/health"
    create_directory(health_dir)

    # __init__.py
    init_content = """
from .symptom_checker import SymptomCheckerSkill
from .diet_planner import DietPlannerSkill
from .fitness_tracker import FitnessTrackerSkill
from .mental_health_assessment import MentalHealthAssessmentSkill
"""
    write_file(os.path.join(health_dir, "__init__.py"), init_content.strip())

    # symptom_checker.py
    symptom_checker_content = """
from aj_mas.skills import BaseSkill, register_skill
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
"""
    write_file(os.path.join(health_dir, "symptom_checker.py"), symptom_checker_content.strip())

    # diet_planner.py
    diet_planner_content = """
from aj_mas.skills import BaseSkill, register_skill
from aj_mas.utils import logger
import random

@register_skill
class DietPlannerSkill(BaseSkill):
    def __init__(self):
        super().__init__("DietPlannerSkill", "Create personalized diet plans")

    def execute(self, parameters: dict) -> dict:
        height = parameters.get('height')
        weight = parameters.get('weight')
        age = parameters.get('age')
        gender = parameters.get('gender')
        goal = parameters.get('goal')
        dietary_restrictions = parameters.get('dietary_restrictions', [])

        logger.log(f"Creating diet plan for {age}-year-old {gender}, height: {height}, weight: {weight}, goal: {goal}")
        
        diet_plan = self._create_diet_plan(height, weight, age, gender, goal, dietary_restrictions)

        result = {"diet_plan": diet_plan}
        self.log_execution(parameters, result)
        return result

    def _create_diet_plan(self, height, weight, age, gender, goal, dietary_restrictions):
        # In a real implementation, this would use nutritional databases and personalized calculations
        bmi = weight / ((height / 100) ** 2)
        
        if bmi < 18.5:
            calorie_adjustment = 500  # Increase calories for underweight
        elif bmi > 25:
            calorie_adjustment = -500  # Decrease calories for overweight
        else:
            calorie_adjustment = 0

        base_calories = 2000 if gender == "female" else 2500
        recommended_calories = base_calories + calorie_adjustment

        meal_plan = {
            "breakfast": ["Oatmeal with fruits", "Greek yogurt with nuts", "Whole grain toast with avocado"],
            "lunch": ["Grilled chicken salad", "Quinoa bowl with vegetables", "Lentil soup with whole grain bread"],
            "dinner": ["Baked salmon with roasted vegetables", "Stir-fry tofu with brown rice", "Lean beef with sweet potato"],
            "snacks": ["Apple with almond butter", "Carrot sticks with hummus", "Mixed nuts"]
        }

        return {
            "recommended_calories": recommended_calories,
            "meal_plan": {meal: random.sample(options, k=3) for meal, options in meal_plan.items()},
            "dietary_advice": f"Focus on {goal}. Ensure to stay hydrated and include a variety of fruits and vegetables.",
            "restrictions_considered": dietary_restrictions
        }
"""
    write_file(os.path.join(health_dir, "diet_planner.py"), diet_planner_content.strip())

    # fitness_tracker.py
    fitness_tracker_content = """
from aj_mas.skills import BaseSkill, register_skill
from aj_mas.utils import logger
import random

@register_skill
class FitnessTrackerSkill(BaseSkill):
    def __init__(self):
        super().__init__("FitnessTrackerSkill", "Track and analyze fitness activities")

    def execute(self, parameters: dict) -> dict:
        activity_type = parameters.get('activity_type')
        duration = parameters.get('duration')
        intensity = parameters.get('intensity')
        user_stats = parameters.get('user_stats', {})

        logger.log(f"Tracking fitness activity: {activity_type} for {duration} minutes at {intensity} intensity")
        
        fitness_analysis = self._analyze_fitness_activity(activity_type, duration, intensity, user_stats)

        result = {"fitness_analysis": fitness_analysis}
        self.log_execution(parameters, result)
        return result

    def _analyze_fitness_activity(self, activity_type, duration, intensity, user_stats):
        # In a real implementation, this would use more accurate fitness formulas and personalized data
        calories_burned_per_minute = {
            "running": 11.4,
            "cycling": 7.5,
            "swimming": 8.3,
            "weightlifting": 6.0
        }.get(activity_type.lower(), 5.0)  # Default to 5.0 for unknown activities

        intensity_multiplier = {"low": 0.8, "medium": 1.0, "high": 1.2}.get(intensity.lower(), 1.0)
        total_calories_burned = calories_burned_per_minute * duration * intensity_multiplier

        return {
            "activity_summary": {
                "type": activity_type,
                "duration": duration,
                "intensity": intensity
            },
            "calories_burned": round(total_calories_burned, 2),
            "health_impact": {
                "cardiovascular": random.choice(["Improved", "Maintained", "Slightly improved"]),
                "muscular": random.choice(["Strengthened", "Toned", "Maintained"]),
                "flexibility": random.choice(["Increased", "Maintained", "Slightly improved"])
            },
            "recommendation": f"Great job on your {activity_type}! Consider increasing duration or intensity for more benefits.",
            "next_goal_suggestion": f"Try to reach {round(duration * 1.1)} minutes in your next {activity_type} session."
        }
"""
    write_file(os.path.join(health_dir, "fitness_tracker.py"), fitness_tracker_content.strip())

    # mental_health_assessment.py
    mental_health_assessment_content = """
from aj_mas.skills import BaseSkill, register_skill
from aj_mas.utils import logger
import random

@register_skill
class MentalHealthAssessmentSkill(BaseSkill):
    def __init__(self):
        super().__init__("MentalHealthAssessmentSkill", "Assess mental health and provide resources")

    def execute(self, parameters: dict) -> dict:
        mood = parameters.get('mood')
        stress_level = parameters.get('stress_level')
        sleep_quality = parameters.get('sleep_quality')
        recent_life_events = parameters.get('recent_life_events', [])

        logger.log(f"Assessing mental health: mood - {mood}, stress level - {stress_level}, sleep quality - {sleep_quality}")
        
        assessment = self._assess_mental_health(mood, stress_level, sleep_quality, recent_life_events)

        result = {"mental_health_assessment": assessment}
        self.log_execution(parameters, result)
        return result

    def _assess_mental_health(self, mood, stress_level, sleep_quality, recent_life_events):
        # In a real implementation, this would use validated psychological assessments and more comprehensive analysis
        mood_score = {"excellent": 5, "good": 4, "neutral": 3, "poor": 2, "very poor": 1}.get(mood.lower(), 3)
        stress_score = {"low": 1, "medium": 2, "high": 3}.get(stress_level.lower(), 2)
        sleep_score = {"good": 3, "fair": 2, "poor": 1}.get(sleep_quality.lower(), 2)

        overall_score = mood_score + (3 - stress_score) + sleep_score

        if overall_score <= 5:
            status = "Concerning"
            recommendations = [
                "Consider speaking with a mental health professional",
                "Practice stress-reduction techniques like meditation",
                "Prioritize sleep and establish a consistent sleep schedule"
            ]
        elif overall_score <= 8:
            status = "Fair"
            recommendations = [
                "Incorporate regular exercise into your routine",
                "Practice mindfulness or relaxation techniques",
                "Reach out to friends or family for support"
            ]
        else:
            status = "Good"
            recommendations = [
                "Maintain your current positive habits",
                "Consider starting a gratitude journal",
                "Explore new hobbies or activities"
            ]

        return {
            "overall_status": status,
            "mood_assessment": f"Your mood is {mood}",
            "stress_assessment": f"Your stress level is {stress_level}",
            "sleep_assessment": f"Your sleep quality is {sleep_quality}",
            "life_events_impact": "Recent life events may be affecting your mental health" if recent_life_events else "No significant recent life events noted",
            "recommendations": recommendations,
            "resources": [
                "National Mental Health Hotline: 1-800-XXX-XXXX",
                "www.mentalhealth.gov",
                "Local community mental health center"
            ],
            "disclaimer": "This assessment is not a substitute for professional medical advice, diagnosis, or treatment."
        }
"""
    write_file(os.path.join(health_dir, "mental_health_assessment.py"), mental_health_assessment_content.strip())

if __name__ == "__main__":
    create_health_skills()
    print("AJ_MAS health skills created successfully!")
