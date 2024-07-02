from ..base_skill import BaseSkill
from ..skill_loader import register_skill
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