# Local Autonomous AI Agent

A local autonomous AI agent that runs on your own computer, similar to Manus but with complete privacy and control. This project integrates DeepSeek R1, Blackbox code generator, and a custom interface to create a powerful AI assistant that can operate autonomously.

## Overview

This project creates a local autonomous AI agent with its own interface window, similar to "Manus Computer" but running entirely on your local machine. It leverages:

- **DeepSeek R1**: A powerful local language model running through Ollama
- **Blackbox Code Generator**: For advanced code generation capabilities
- **Custom Tkinter Interface**: A clean, modern UI for interacting with the agent

The agent can understand complex instructions, break them down into steps, and execute them autonomously while providing clear explanations of its actions.

## Features

- **Fully Local Operation**: All processing happens on your machine, ensuring privacy and control
- **Autonomous Task Execution**: The agent can break down complex tasks and execute them step by step
- **Code Generation**: Integrated with Blackbox for powerful code generation capabilities
- **Modern Interface**: Clean, intuitive UI with chat history, task monitoring, and tool windows
- **Extensible Architecture**: Modular design allows for easy addition of new capabilities

## Prerequisites

- **Windows** with WSL Ubuntu setup
- **Python 3.8+** installed
- **VS Code** with Blackbox extension installed
- **Ollama** installed for running DeepSeek R1 locally
- At least **8GB RAM** (16GB+ recommended)
- At least **10GB free storage** space
- **GPU** (optional but recommended for faster model inference)

## Installation

1. **Install Ollama**:
   - Visit [ollama.com/download](https://ollama.com/download) and follow the installation instructions for your OS

2. **Pull DeepSeek R1 Model**:
   ```bash
   ollama pull deepseek-r1:8b
   ```

3. **Install VS Code and Blackbox Extension**:
   - Install VS Code from [code.visualstudio.com](https://code.visualstudio.com/)
   - Open VS Code and install the Blackbox extension from the marketplace

4. **Clone this Repository**:
   ```bash
   git clone https://github.com/yourusername/local-autonomous-ai-agent.git
   cd local-autonomous-ai-agent
   ```

5. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start Ollama**:
   - Make sure Ollama is running in the background

2. **Launch the Agent**:
   ```bash
   python auto_agent_gui.py
   ```

3. **Interact with the Agent**:
   - Type your requests in the input field and press Enter or click Send
   - The agent will process your request and provide a response
   - For complex tasks, the agent will break them down and execute them step by step

## Project Structure

- `auto_agent_gui.py`: Main application with Tkinter GUI
- `deepseek_integration.py`: Module for integrating with DeepSeek R1 through Ollama
- `blackbox_integration.py`: Module for integrating with Blackbox code generator
- `local_autonomous_ai_agent_design.md`: Detailed design document

## Customization

### Changing the Model

You can use different DeepSeek R1 model sizes based on your hardware capabilities:

- `deepseek-r1:1.5b`: Smallest model, fastest but least capable
- `deepseek-r1:7b`: Good balance of speed and capability
- `deepseek-r1:8b`: Default model, good balance of speed and capability
- `deepseek-r1:14b`: More capable but requires more RAM
- `deepseek-r1:32b`: Very capable but requires significant RAM
- `deepseek-r1:70b`: Most capable but requires high-end hardware

To change the model, use the Model Settings dialog in the application or modify the `model_name` parameter in the code.

### Adding New Tools

The agent is designed to be extensible. To add new tools:

1. Create a new Python module for your tool
2. Implement the necessary functions for integration
3. Add the tool to the Tools menu in `auto_agent_gui.py`
4. Update the agent's system prompt to include information about the new tool

## Troubleshooting

### Ollama Connection Issues

If the agent cannot connect to Ollama:

1. Make sure Ollama is running (`ollama serve`)
2. Check if the DeepSeek R1 model is installed (`ollama list`)
3. If not installed, pull the model (`ollama pull deepseek-r1:8b`)

### VS Code and Blackbox Issues

If the Blackbox integration is not working:

1. Make sure VS Code is installed and accessible from the command line
2. Verify that the Blackbox extension is installed in VS Code
3. Check the extension settings and ensure it's properly configured

### Performance Issues

If the agent is running slowly:

1. Try using a smaller model (e.g., `deepseek-r1:7b` instead of `deepseek-r1:8b`)
2. Close other resource-intensive applications
3. If available, ensure your GPU is being utilized

## Future Enhancements

- **Multi-agent Collaboration**: Enable multiple specialized agents to work together
- **Voice Interface**: Add speech recognition and synthesis for voice interaction
- **Advanced Tool Integration**: Integrate with more external tools and APIs
- **Improved Memory Management**: Enhance context retention and knowledge retrieval
- **Custom Plugin System**: Allow users to create and install their own plugins

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- DeepSeek AI for the DeepSeek R1 model
- Blackbox AI for the code generation capabilities
- Ollama for the local model serving framework

