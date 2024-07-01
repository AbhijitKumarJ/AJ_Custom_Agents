import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def create_file(path):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write("# Placeholder\n")
        print(f"Created file: {path}")

def create_project_structure():
    root_dir = "aj_mas"
    create_directory(root_dir)

    # Create main directories
    directories = [
        "agents", "skills", "tools", "models", "utils", "personas", "document_store", "config"
    ]
    for directory in directories:
        create_directory(os.path.join(root_dir, directory))

    # Create skill subdirectories
    skill_subdirs = ["travel", "finance", "health", "legal", "technology"]
    for subdir in skill_subdirs:
        create_directory(os.path.join(root_dir, "skills", subdir))

    # Create tool subdirectories
    tool_subdirs = ["web_interaction", "data_analysis", "nlp", "file_handling"]
    for subdir in tool_subdirs:
        create_directory(os.path.join(root_dir, "tools", subdir))

    # Create placeholder files
    placeholder_files = [
        # Agents
        "agents/__init__.py",
        "agents/base_agent.py",
        "agents/persona_based_agent.py",
        "agents/specialized_agents.py",
        "agents/agent_factory.py",

        # Skills
        "skills/__init__.py",
        "skills/base_skill.py",
        "skills/skill_loader.py",
    ] + [
        f"skills/{subdir}/__init__.py" for subdir in skill_subdirs
    ] + [
        # Tools
        "tools/__init__.py",
        "tools/base_tool.py",
        "tools/tool_loader.py",
    ] + [
        f"tools/{subdir}/__init__.py" for subdir in tool_subdirs
    ] + [
        # Models
        "models/__init__.py",
        "models/model_provider.py",
        "models/ollama_provider.py",
        "models/huggingface_provider.py",

        # Utils
        "utils/__init__.py",
        "utils/logger.py",
        "utils/config_loader.py",
        "utils/error_handler.py",

        # Personas
        "personas/__init__.py",
        "personas/persona.py",
        "personas/persona_loader.py",

        # Document Store
        "document_store/__init__.py",
        "document_store/document_store.py",
        "document_store/fasttext_chroma_store.py",

        # Config
        "config/config.json",
        "config/agent_config.json",
        "config/skill_config.json",
        "config/tool_config.json",

        # Root directory files
        "main.py",
        "requirements.txt",
        "README.md",
    ]

    for file_path in placeholder_files:
        create_file(os.path.join(root_dir, file_path))

if __name__ == "__main__":
    create_project_structure()
    print("AJ_MAS project structure created successfully!")
