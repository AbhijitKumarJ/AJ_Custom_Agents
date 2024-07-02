from ..base_skill import BaseSkill
from ..skill_loader import register_skill
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