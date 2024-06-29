import os
import json

def create_file(path, content=''):
    with open(path, 'w') as f:
        f.write(content)

def create_folder_structure():
    base_dir = 'react_agent'
    os.makedirs(base_dir, exist_ok=True)

    # Create main files
    create_file(os.path.join(base_dir, '__init__.py'), 'from .main import AdvancedReActAgent')
    create_file(os.path.join(base_dir, 'main.py'), '# Main ReAct Agent implementation')
    create_file(os.path.join(base_dir, 'config.py'), '# Configuration settings')

    # Create NLP folder and files
    nlp_dir = os.path.join(base_dir, 'nlp')
    os.makedirs(nlp_dir, exist_ok=True)
    create_file(os.path.join(nlp_dir, '__init__.py'))
    create_file(os.path.join(nlp_dir, 'intent_classifier.py'), '# Intent classification implementation')
    create_file(os.path.join(nlp_dir, 'parameter_extractor.py'), '# Parameter extraction implementation')

    # Create actions folder and files
    actions_dir = os.path.join(base_dir, 'actions')
    os.makedirs(actions_dir, exist_ok=True)
    create_file(os.path.join(actions_dir, '__init__.py'))
    create_file(os.path.join(actions_dir, 'weather.py'), '# Weather action implementation')
    create_file(os.path.join(actions_dir, 'time_info.py'), '# Time action implementation')
    create_file(os.path.join(actions_dir, 'jokes.py'), '# Jokes action implementation')
    create_file(os.path.join(actions_dir, 'general.py'), '# General actions implementation')

    # Create utils folder and files
    utils_dir = os.path.join(base_dir, 'utils')
    os.makedirs(utils_dir, exist_ok=True)
    create_file(os.path.join(utils_dir, '__init__.py'))
    create_file(os.path.join(utils_dir, 'logger.py'), '# Logger implementation')

    # Create data folder and jokes.json
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "Why don't skeletons fight each other? They don't have the guts!",
        "What do you call a fake noodle? An impasta!"
    ]
    create_file(os.path.join(data_dir, 'jokes.json'), json.dumps(jokes, indent=2))

    print("Folder structure created successfully!")

if __name__ == "__main__":
    create_folder_structure()