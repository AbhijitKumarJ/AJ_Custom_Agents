# Multi-Agent System with RAG-like Document Retrieval

This project implements a configurable multi-agent system capable of performing various tasks using different skills and models. It includes a RAG-like (Retrieval-Augmented Generation) document retrieval system that allows users to add text files to enhance the conversation context.


Current State: There are issue with some task processing which i am trying to fix

## Table of Contents

1. [Features](#features)
2. [Setup](#setup)
3. [Configuration](#configuration)
4. [Running the System](#running-the-system)
5. [System Architecture](#system-architecture)
6. [Adding New Skills](#adding-new-skills)
7. [Adding New Agents](#adding-new-agents)
8. [Document Retrieval System](#document-retrieval-system)
9. [Memory System](#memory-system)
10. [Extending the System](#extending-the-system)
11. [Troubleshooting](#troubleshooting)
12. [Contributing](#contributing)
13. [License](#license)
14. [Acknowledgments](#acknowledgments)

## Features

- Modular architecture with extensible skills and agents
- RAG-like document retrieval for enhanced context
- Conversational memory system
- Configurable model selection (Ollama API or Hugging Face Transformers)
- Task analysis and decomposition
- Logging system for debugging and monitoring

## Setup

1. Clone this repository:
   ```
   git clone <repository-url>
   cd multi-agent-system
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. If you're using the Ollama API, make sure Ollama is installed and the desired model is pulled:
   ```
   ollama pull qwen:1.5b
   ```

5. Start the Ollama server (if using Ollama):
   ```
   ollama serve
   ```

## Configuration

The system behavior can be configured by modifying the `config.json` file. Key configuration options include:

- `model`: Specifies the language model to use for task analysis and generation.
- `skills`: Enables or disables specific skills.
- `agents`: Configures the available agent types.
- `memory_system`: Sets the file for storing conversation history.
- `document_store`: Configures the directory for storing added documents.
- `logging`: Sets the logging level and output file.

## Running the System

To run the multi-agent system:

```
python main.py
```

Follow the prompts to interact with the system. You can:
- Enter your user ID
- Add documents to the knowledge base
- Perform tasks
- End your session

## System Architecture

The system consists of several key components:

1. **Skills**: Modular capabilities that agents can use (e.g., math, language processing).
2. **Agents**: Entities that use skills to perform tasks.
3. **Task Analyzer**: Breaks down complex tasks into subtasks.
4. **Document Store**: Manages the storage and retrieval of added documents.
5. **Memory System**: Maintains conversation history across sessions.
6. **Logger**: Provides system-wide logging capabilities.

## Adding New Skills

To add a new skill:

1. Create a new file in the `skills` directory named `your_skill_name_skill.py`.
2. Implement a new class that inherits from `BaseSkill`.
3. Implement the `execute` method and any necessary helper methods.
4. Update the `config.json` file to include your new skill.
5. The system will automatically detect and load your new skill.

## Adding New Agents

To add a new agent:

1. Create a new file in the `agents` directory named `your_agent_name_agent.py`.
2. Implement a new class that inherits from `BaseAgent`.
3. Implement the `perform_task` method and any necessary helper methods.
4. Update the `config.json` file to include your new agent.
5. The system will automatically detect and load your new agent.

## Document Retrieval System

The document retrieval system allows users to add text files to enhance the conversation context:

- Users can add documents using the 'add_document' action.
- Documents are indexed using TF-IDF vectorization.
- Relevant document snippets are retrieved based on cosine similarity to the user's task.
- Retrieved information is incorporated into the task context for improved responses.

## Memory System

The memory system maintains conversation history across sessions:

- Each user has a separate conversation history.
- Recent conversations are used to provide context for new tasks.
- The system can refer to past interactions to maintain consistency and context.

## Extending the System

To extend the system's capabilities:

1. **New Document Types**: Modify the `DocumentStore` class to support additional file formats.
2. **Advanced Retrieval**: Implement more sophisticated retrieval algorithms in the `DocumentStore` class.
3. **Enhanced Task Analysis**: Improve the `TaskAnalyzer` class with more advanced NLP techniques.
4. **User Interface**: Develop a graphical user interface or web interface for easier interaction.

## Troubleshooting

If you encounter issues:

1. Check the log file specified in `config.json` for detailed error messages.
2. Ensure all dependencies are correctly installed.
3. Verify that the configuration in `config.json` is correct and all referenced models are available.
4. For Ollama-related issues, ensure the Ollama server is running and the specified model is available.

## Contributing

Contributions to this project are welcome! Here's how you can contribute:

1. Fork the repository and create your branch from `main`.
2. Make your changes and ensure the code lints.
3. Add or update tests as necessary.
4. Update the documentation to reflect your changes.
5. Submit a pull request with a comprehensive description of changes.

Please adhere to the project's coding standards and include appropriate tests and documentation with your contributions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses the Hugging Face Transformers library for natural language processing tasks.
- The RAG-like feature is inspired by the Retrieval-Augmented Generation paper by Lewis et al.
- Thanks to the Ollama project for providing easy access to large language models.

For more information or support, please open an issue on the GitHub repository.
