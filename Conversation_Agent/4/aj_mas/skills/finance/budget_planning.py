from ..base_skill import BaseSkill
from ..skill_loader import register_skill
from aj_mas.utils import logger
import random

@register_skill
class BudgetPlanningSkill(BaseSkill):
    def __init__(self):
        super().__init__("BudgetPlanningSkill", "Create and analyze budgets")

    def execute(self, parameters: dict) -> dict:
        income = parameters.get('income')
        expenses = parameters.get('expenses', {})
        savings_goal = parameters.get('savings_goal')

        logger.log(f"Creating budget plan for income ${income} and savings goal ${savings_goal}")
        
        budget_plan = self._create_budget_plan(income, expenses, savings_goal)

        result = {"budget_plan": budget_plan}
        self.log_execution(parameters, result)
        return result

    def _create_budget_plan(self, income, expenses, savings_goal):
        # In a real implementation, this would use more sophisticated budgeting algorithms
        total_expenses = sum(expenses.values())
        available_for_savings = income - total_expenses

        if available_for_savings >= savings_goal:
            status = "On Track"
            recommendations = ["Consider increasing your savings goal", "Look into investment opportunities"]
        else:
            status = "Needs Adjustment"
            deficit = savings_goal - available_for_savings
            recommendations = [
                f"Reduce expenses by ${deficit:.2f} to meet your savings goal",
                "Look for additional income sources",
                "Prioritize expenses and cut non-essential spending"
            ]

        return {
            "income": income,
            "total_expenses": total_expenses,
            "available_for_savings": available_for_savings,
            "savings_goal": savings_goal,
            "status": status,
            "recommendations": recommendations
        }