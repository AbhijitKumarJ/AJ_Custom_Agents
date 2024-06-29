# Main ReAct Agent implementation
from .nlp.intent_classifier import IntentClassifier
from .nlp.parameter_extractor import ParameterExtractor
from .actions import WeatherAction, TimeAction, JokeAction, GeneralAction
from .utils.logger import Logger
from .config import CONTEXT_SIZE

class AdvancedReActAgent:
    def __init__(self):
        self.context = []
        self.intent_classifier = IntentClassifier()
        self.parameter_extractor = ParameterExtractor()
        self.actions = {
            'get_weather': WeatherAction(),
            'ask_time': TimeAction(),
            'tell_joke': JokeAction(),
            'greet': GeneralAction(),
            'farewell': GeneralAction(),
            'unknown': GeneralAction()
        }
        Logger.log("AdvancedReActAgent initialized")

    def think(self, user_input: str):
        Logger.log("Thinking process started", {"input": user_input})
        intent_info = self.intent_classifier.classify_intent(user_input)
        parameters = self.parameter_extractor.extract_parameters(user_input, intent_info['action'])
        
        thoughts = [
            ("Intent", f"Action determined as: {intent_info['action']} with confidence {intent_info['confidence']:.2f}"),
            ("Parameters", f"Extracted parameters: {parameters}")
        ]
        
        action_info = {**intent_info, "parameters": parameters}
        Logger.log("Thinking process completed", {"thoughts": thoughts, "action_info": action_info})
        return thoughts, action_info

    def act(self, action_info: dict) -> str:
        Logger.log("Acting", action_info)
        action = self.actions.get(action_info['action'], self.actions['unknown'])
        response = action.execute(action_info['parameters'])
        Logger.log("Action completed", {"response": response})
        return response

    def respond(self, user_input: str) -> str:
        Logger.log("Responding to user input", {"input": user_input})
        thoughts, action_info = self.think(user_input)
        response = self.act(action_info)
        self.update_context(user_input)
        Logger.log("Response generated", {"response": response, "updated_context": self.context})
        return response

    def update_context(self, user_input: str):
        self.context.append(user_input)
        if len(self.context) > CONTEXT_SIZE:
            self.context.pop(0)

    def run(self):
        Logger.log("Starting the agent")
        print("Advanced ReAct Agent: Hello! How can I assist you today?")
        while True:
            user_input = input("You: ")
            Logger.log("Received user input", {"input": user_input})
            if user_input.lower() == "quit":
                Logger.log("User requested to quit")
                print("Advanced ReAct Agent: Goodbye!")
                break
            response = self.respond(user_input)
            print(f"Advanced ReAct Agent: {response}")
        Logger.log("Agent shutting down")

if __name__ == "__main__":
    agent = AdvancedReActAgent()
    agent.run()