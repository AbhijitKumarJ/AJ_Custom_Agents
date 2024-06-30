import os
import json

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def create_file(path, content=''):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Created file: {path}")

def setup_project():
    # Create main project directory
    project_dir = "multi_agent_system"
    create_directory(project_dir)

    # Create subdirectories
    subdirs = ["agents", "skills", "utils", "document_storage"]
    for subdir in subdirs:
        create_directory(os.path.join(project_dir, subdir))

    # Create __init__.py files
    init_dirs = ["agents", "skills", "utils"]
    for dir in init_dirs:
        create_file(os.path.join(project_dir, dir, "__init__.py"))

    # Create main.py
    main_content = """
from skills.skill_loader import ALL_SKILLS
from agents.agent_loader import ALL_AGENTS
from utils import logger, config
import os

class MultiAgentSystem:
    def __init__(self):
        # Initialization code here

    def run(self):
        # Main run loop here

if __name__ == "__main__":
    system = MultiAgentSystem()
    system.run()
"""
    create_file(os.path.join(project_dir, "main.py"), main_content)

    # Create config.json
    config = {
        "model": {
            "name": "qwen:1.5b",
            "type": "ollama",
            "huggingface_repo": "Qwen/Qwen1.5-1.8B",
            "max_length": 100,
            "temperature": 0.7
        },
        "ollama": {
            "api_url": "http://localhost:11434/api/generate"
        },
        "task_analyzer": {
            "prompt_template": "Given the following task, extract the relevant parameters and subtasks:\nTask: {task}\n\nProvide the output in the following JSON format:\n{\n    \"subtasks\": [\"list of subtasks\"],\n    \"parameters\": {\n        \"param1\": \"value1\",\n        \"param2\": \"value2\"\n    }\n}"
        },
        "skills": {
            "math": {"enabled": True},
            "language": {
                "enabled": True,
                "translation_model": "t5-small"
            },
            "numbergeneration": {"enabled": True}
        },
        "agents": {
            "standard": {"enabled": True},
            "primary": {"enabled": True}
        },
        "memory_system": {
            "file": "conversation_memory.json"
        },
        "document_store": {
            "storage_dir": "document_storage"
        },
        "logging": {
            "level": "INFO",
            "file": "multi_agent_system.log"
        }
    }
    create_file(os.path.join(project_dir, "config.json"), json.dumps(config, indent=2))

    # Create README.md
    readme_content = """
# Multi-Agent System with RAG-like Document Retrieval

This is a configurable multi-agent system that can perform various tasks using different skills and models. It includes a RAG-like document retrieval system that allows users to add text files to enhance the conversation context.

## Setup

[Setup instructions here]

## Running the System

To run the multi-agent system:

```
python main.py
```

[Additional instructions here]
"""
    create_file(os.path.join(project_dir, "README.md"), readme_content)

    # Create requirements.txt
    requirements = """
torch
transformers
pyyaml
requests
scikit-learn
"""
    create_file(os.path.join(project_dir, "requirements.txt"), requirements)

    # Create agent files
    agent_files = {
        "base_agent.py": "# Base agent implementation",
        "standard_agent.py": "# Standard agent implementation",
        "primary_agent.py": "# Primary agent implementation",
        "agent_loader.py": "# Agent loader implementation"
    }
    for filename, content in agent_files.items():
        create_file(os.path.join(project_dir, "agents", filename), content)

    # Create skill files
    skill_files = {
        "base_skill.py": "# Base skill implementation",
        "math_skill.py": "# Math skill implementation",
        "language_skill.py": "# Language skill implementation",
        "number_generation_skill.py": "# Number generation skill implementation",
        "skill_loader.py": "# Skill loader implementation"
    }
    for filename, content in skill_files.items():
        create_file(os.path.join(project_dir, "skills", filename), content)

    # Create utility files
    util_files = {
        "logger.py": "# Logger implementation",
        "memory_system.py": "# Memory system implementation",
        "document_store.py": "# Document store implementation",
        "task_analyzer.py": "# Task analyzer implementation"
    }
    for filename, content in util_files.items():
        create_file(os.path.join(project_dir, "utils", filename), content)

    print("Project setup complete!")

if __name__ == "__main__":
    setup_project()
