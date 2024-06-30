import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from .base_skill import BaseSkill
from ..utils.logger import logger
from ..config import config


class LanguageSkill(BaseSkill):
    def __init__(self):
        super().__init__("Language", "Perform language-related tasks")
        model_name = (
            config.get("skills", {})
            .get("language", {})
            .get("translation_model", "t5-small")
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        logger.log(
            f"Initialized translation model",
            {"model": model_name, "device": self.device},
        )

    def execute(self, subtask, **kwargs):
        logger.log(f"Executing Language Skill", {"subtask": subtask, "kwargs": kwargs})
        if subtask == "count_words":
            result = len(kwargs.get("text", "").split())
        elif subtask == "reverse":
            result = kwargs.get("text", "")[::-1]
        elif subtask == "translate":
            if not kwargs.get("target_language"):
                raise ValueError("Target language is required for translation")
            result = self.translate(
                kwargs.get("text", ""), kwargs.get("target_language")
            )
        else:
            result = f"Unsupported subtask: {subtask}"
        logger.log(f"Language Skill Result", {"result": result})
        return result

    def translate(self, text, target_language):
        logger.log(
            f"Translating text", {"text": text, "target_language": target_language}
        )
        input_text = f"translate English to {target_language}: {text}"
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(
            self.device
        )
        outputs = self.model.generate(
            input_ids, max_length=40, num_beams=4, early_stopping=True
        )
        translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.log(f"Translation Result", {"translated_text": translated_text})
        return translated_text
