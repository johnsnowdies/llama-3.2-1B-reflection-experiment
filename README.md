# AI Self-Reflection Experiment

This project implements an AI-driven self-reflection experiment where two language models engage in a conversation, asking and answering questions to explore self-awareness and identity.

## Overview

The experiment consists of two AI agents:

1. **Inquirer (A)**: Asks questions and analyzes responses
2. **Respondent (B)**: Answers questions and provides introspective insights

These agents engage in an iterative conversation, with each iteration involving a question from the Inquirer and a response from the Respondent.

## Features

- Configurable number of conversation iterations
- Logging of the entire conversation to a timestamped file
- Dynamic conversation management to stay within token limits
- Ability to pause and request human input during the experiment
- Graceful experiment termination upon request from either AI agent

## Requirements

- Python 3.7+
- `requests` library
- Access to a compatible language model API (e.g., OpenAI GPT)

## Configuration
Adjust the following parameters in `main.py` to customize the experiment:

- `NUM_ITERATIONS`: Number of conversation rounds
- `MAX_TOKENS`: Maximum tokens for conversation history
- `MODEL`: The language model to use
- `SYSTEM_PROMPT_A` and `SYSTEM_PROMPT_B`: System prompts for Inquirer and Respondent

## Output

The conversation is logged to a file named `self_reflection_log_YYYY-MM-DD HH:MM:SS.txt` in the project directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.