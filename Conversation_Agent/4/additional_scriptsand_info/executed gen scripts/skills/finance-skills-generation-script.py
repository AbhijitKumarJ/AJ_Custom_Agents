import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def create_finance_skills():
    finance_dir = "aj_mas/skills/finance"
    create_directory(finance_dir)

    # __init__.py
    init_content = """
from .investment_analysis import InvestmentAnalysisSkill
from .budget_planning import BudgetPlanningSkill
from .tax_calculation import TaxCalculationSkill
from .stock_prediction import StockPredictionSkill
"""
    write_file(os.path.join(finance_dir, "__init__.py"), init_content.strip())

    # investment_analysis.py
    investment_analysis_content = """
from aj_mas.skills import BaseSkill, register_skill
from aj_mas.utils import logger
import random

@register_skill
class InvestmentAnalysisSkill(BaseSkill):
    def __init__(self):
        super().__init__("InvestmentAnalysisSkill", "Analyze investment opportunities")

    def execute(self, parameters: dict) -> dict:
        investment_type = parameters.get('investment_type')
        amount = parameters.get('amount')
        risk_tolerance = parameters.get('risk_tolerance')

        logger.log(f"Analyzing {investment_type} investment of ${amount} with {risk_tolerance} risk tolerance")
        
        analysis = self._analyze_investment(investment_type, amount, risk_tolerance)

        result = {"analysis": analysis}
        self.log_execution(parameters, result)
        return result

    def _analyze_investment(self, investment_type, amount, risk_tolerance):
        # In a real implementation, this would use financial models and market data
        expected_return = random.uniform(0.02, 0.15)
        risk_level = random.choice(["Low", "Medium", "High"])
        recommendation = random.choice(["Buy", "Hold", "Sell"])

        return {
            "expected_return": f"{expected_return:.2%}",
            "risk_level": risk_level,
            "recommendation": recommendation,
            "summary": f"For a {investment_type} investment of ${amount} with {risk_tolerance} risk tolerance, "
                       f"we expect a return of {expected_return:.2%}. The risk level is considered {risk_level}. "
                       f"Our recommendation is to {recommendation}."
        }
"""
    write_file(os.path.join(finance_dir, "investment_analysis.py"), investment_analysis_content.strip())

    # budget_planning.py
    budget_planning_content = """
from aj_mas.skills import BaseSkill, register_skill
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
"""
    write_file(os.path.join(finance_dir, "budget_planning.py"), budget_planning_content.strip())

    # tax_calculation.py
    tax_calculation_content = """
from aj_mas.skills import BaseSkill, register_skill
from aj_mas.utils import logger

@register_skill
class TaxCalculationSkill(BaseSkill):
    def __init__(self):
        super().__init__("TaxCalculationSkill", "Calculate estimated taxes")

    def execute(self, parameters: dict) -> dict:
        income = parameters.get('income')
        deductions = parameters.get('deductions', [])
        filing_status = parameters.get('filing_status')

        logger.log(f"Calculating taxes for ${income} income with {filing_status} filing status")
        
        tax_calculation = self._calculate_taxes(income, deductions, filing_status)

        result = {"tax_calculation": tax_calculation}
        self.log_execution(parameters, result)
        return result

    def _calculate_taxes(self, income, deductions, filing_status):
        # This is a simplified tax calculation. In a real implementation, 
        # this would use actual tax brackets and more complex rules
        total_deductions = sum(deductions)
        taxable_income = max(0, income - total_deductions)

        if filing_status == "single":
            tax_rate = 0.22  # Simplified tax rate
        elif filing_status == "married":
            tax_rate = 0.18  # Simplified tax rate
        else:
            tax_rate = 0.20  # Default rate

        estimated_tax = taxable_income * tax_rate

        return {
            "total_income": income,
            "total_deductions": total_deductions,
            "taxable_income": taxable_income,
            "estimated_tax": estimated_tax,
            "effective_tax_rate": estimated_tax / income if income > 0 else 0
        }
"""
    write_file(os.path.join(finance_dir, "tax_calculation.py"), tax_calculation_content.strip())

    # stock_prediction.py
    stock_prediction_content = """
from aj_mas.skills import BaseSkill, register_skill
from aj_mas.utils import logger
import random

@register_skill
class StockPredictionSkill(BaseSkill):
    def __init__(self):
        super().__init__("StockPredictionSkill", "Predict stock price movements")

    def execute(self, parameters: dict) -> dict:
        stock_symbol = parameters.get('stock_symbol')
        prediction_period = parameters.get('prediction_period')

        logger.log(f"Predicting stock price for {stock_symbol} over {prediction_period}")
        
        prediction = self._predict_stock_price(stock_symbol, prediction_period)

        result = {"prediction": prediction}
        self.log_execution(parameters, result)
        return result

    def _predict_stock_price(self, stock_symbol, prediction_period):
        # In a real implementation, this would use machine learning models and market data
        current_price = random.uniform(10, 1000)
        predicted_change = random.uniform(-0.2, 0.2)
        predicted_price = current_price * (1 + predicted_change)

        confidence = random.uniform(0.5, 0.9)
        factors = ["Market trends", "Company financials", "Industry outlook", "Economic indicators"]
        considered_factors = random.sample(factors, k=random.randint(2, len(factors)))

        return {
            "stock_symbol": stock_symbol,
            "current_price": current_price,
            "predicted_price": predicted_price,
            "predicted_change_percentage": predicted_change * 100,
            "prediction_period": prediction_period,
            "confidence": confidence,
            "considered_factors": considered_factors,
            "recommendation": "Buy" if predicted_change > 0 else "Sell"
        }
"""
    write_file(os.path.join(finance_dir, "stock_prediction.py"), stock_prediction_content.strip())

if __name__ == "__main__":
    create_finance_skills()
    print("AJ_MAS finance skills created successfully!")
