from ..base_skill import BaseSkill
from ..skill_loader import register_skill
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