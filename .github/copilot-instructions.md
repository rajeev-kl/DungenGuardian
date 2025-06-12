<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Dungeon Guardian Agent Project
- This project is for developing an AI agent to act as a dungeon guardian.
- Use Python best practices and structure code for easy extension with AI/ML libraries.
- Include clear docstrings and comments for all major functions and classes.
- Organize code into modules: environment, agent, training, and utils.
- Write unit tests for core logic.

## Project File Structure Reference

- `main.py`: Entry point, CLI, scenario runners, and output-to-clipboard logic.
- `agent/`
  - `__init__.py`: Agent module init.
  - `cognitive.py`: LLM-style reasoning and cognitive layer.
  - `planning.py`: GOAP symbolic planning and special mode logic.
- `environment/`
  - `__init__.py`: Dungeon environment simulation.
- `training/`
  - `__init__.py`: Training and scenario execution logic.
- `utils/`
  - `__init__.py`: Utility functions (e.g., print_banner).
- `goap_actions.ini`: GOAP action definitions.
- `hell_mode_scenario.json`: Obfuscated special mode scenario.
- `true_multistep_scenarios.json`: Batch test scenarios.
- `README.md`: Project overview and usage.
- `Pipfile`, `Pipfile.lock`, `pyproject.toml`: Dependency management.

## Code Flow Reference

1. **Startup**: `main.py` parses CLI args, selects mode (interactive, batch, or default).
2. **Scenario Execution**: Runs agent/environment logic, captures output.
3. **Output Handling**: After batch/special runs, output is auto-copied to clipboard for easy Copilot Chat use.
4. **Copilot Reasoning**: User pastes output into Copilot Chat in VS Code for LLM-style analysis.


