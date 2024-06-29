# Intent classification implementation

from transformers import pipeline
from ..utils.logger import Logger
from ..config import INTENT_MODEL, ACTION_TEMPLATES

class IntentClassifier:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification", model=INTENT_MODEL)
        self.action_templates = ACTION_TEMPLATES
        Logger.log("IntentClassifier initialized", {"model": INTENT_MODEL, "templates": self.action_templates})

    def classify_intent(self, user_input: str) -> dict:
        Logger.log("Classifying intent", {"input": user_input})
        candidate_labels = [template for template, _ in self.action_templates]
        outputs = self.classifier(user_input, candidate_labels, multi_label=False)
        
        Logger.log("Classification model raw output", outputs)

        best_action_label = outputs["labels"][0]
        best_action_score = outputs["scores"][0]

        action = next((action for template, action in self.action_templates if template == best_action_label), "unknown")

        result = {"action": action, "confidence": best_action_score}
        Logger.log("Classification result", result)
        return result