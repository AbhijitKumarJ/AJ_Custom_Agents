# Jokes action implementation
import json
import random
from ..utils.logger import Logger

class JokeAction:
    def __init__(self):
        with open('RA_Lib/data/jokes.json', 'r') as f:
            self.jokes = json.load(f)
        self.told_jokes = set()

    def execute(self, params: dict) -> str:
        Logger.log("Telling a joke")
        
        available_jokes = [joke for joke in self.jokes if joke not in self.told_jokes]
        
        if not available_jokes:
            self.told_jokes.clear()
            available_jokes = self.jokes
        
        joke = random.choice(available_jokes)
        self.told_jokes.add(joke)
        
        return joke