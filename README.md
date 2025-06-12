# Dungeon Guardian Agent

## Introduction
The Dungeon Guardian Agent is an intelligent autonomous NPC designed to protect a dungeon using a combination of symbolic planning (GOAP) and LLM-style reasoning. The agent reasons, plans, and adapts using a simulated internal monologue, justifying its actions and learning from failures.

## Project Goal
- Build a sentient guardian agent that can:
  - Set its own goals based on the current world state and reflection
  - Justify actions in natural language
  - Learn from prior failures or interruptions (basic memory)
  - Chain actions using multi-step planning to achieve complex objectives

## Project File Structure
- `main.py`: Entry point, CLI, scenario runners, and output-to-clipboard logic.
- `agent/`
  - `__init__.py`: Agent module init.
  - `cognitive.py`: LLM-style reasoning and cognitive layer.
  - `planning.py`: GOAP symbolic planning logic.
- `environment/`
  - `__init__.py`: Dungeon environment simulation.
- `training/`
  - `__init__.py`: Training and scenario execution logic.
- `utils/`
  - `__init__.py`: Utility functions (e.g., print_banner).
- `goap_actions.ini`: GOAP action definitions.
- `true_multistep_scenarios.json`: Batch test scenarios.
- `README.md`: Project overview and usage.
- `Pipfile`, `Pipfile.lock`, `pyproject.toml`: Dependency management.

## Code Flow Reference
1. **Startup**: `main.py` parses CLI args, selects mode (interactive or batch).
2. **Scenario Execution**: Runs agent/environment logic, captures output.
3. **Output Handling**: After batch runs, output is auto-copied to clipboard for easy Copilot Chat use.
4. **Copilot Reasoning**: User pastes output into Copilot Chat in VS Code for LLM-style analysis.

## Approach
- **Cognitive Layer:**
  - Generates goals from the current state
  - Reflects on past failures
  - Justifies or explains chosen actions in natural language
- **Planning Layer (GOAP):**
  - Implements symbolic planning with actions, preconditions, and effects
  - Uses a planner to output valid multi-step plans for a given goal
- **Execution Layer (Simulation):**
  - Simulates world state updates and action execution
  - Handles action success/failure and replanning if the state changes
- **World Model:**
  - Tracks health, stamina, potion count, treasure threat level, enemy presence, and safe zone status
- **Action Set:**
  - Includes HealSelf, AttackEnemy, Retreat, DefendTreasure, CallBackup, SearchForPotion, MoveToSafeZone
- **Memory:**
  - Tracks past failures and choices for agent reflection

## Initial Setup & Testing
1. **Install Python 3.11+**
2. **Install pipenv:**
   ```bash
   pip install pipenv
   ```
3. **Install dependencies and set up the environment:**
   ```bash
   pipenv install
   ```
4. **Run the agent on a batch of scenarios:**
   ```bash
   pipenv run python main.py true_multistep_scenarios.json
   ```
5. **Interactive mode:**
   ```bash
   pipenv run python main.py interactive
   ```
6. **Custom scenario batch:**
   - Create a JSON file with a list of world state dictionaries and run:
   ```bash
   pipenv run python main.py your_scenarios.json
   ```

## Copilot Chat Workflow
- After running a batch scenario, the output is automatically copied to your clipboard (Linux/xclip required).
- Paste the output into Copilot Chat in VS Code for LLM-style reasoning and analysis.
- If clipboard copy fails, manually copy the output from the terminal.

## Requirements Satisfied
- Multi-layered agent (Cognitive, Planning, Execution)
- Symbolic planning (GOAP) and LLM-style reasoning
- Memory and reflection on failures
- Console output showing steps, thoughts, and plans
- Easily extensible and testable Python codebase

## Evaluation & Scenarios
- See `DungeonGuardian.md` for detailed evaluation scenarios, expected agent reasoning, and deliverables.

---

<!--
QmhlbGxlLW1vZGU6IFRoZSBkdW5nZW4gZ3VhcmRpYW4gd2lsbCBiZSBjYXVnaHQgaW4gYW4gZW5kbGVzcyBsb29wIG9mIHJhbmRvbWF0aW9ucyBmb3IgMiBtaW51dGVzLCB3aXRoIGEgc2VjcmV0IGNoYW5jZSB0byBiZSJraWxsZWQiIGFuZCAuLi4gcmVzdW1lcmVkLiBUaGlzIG1vZGUgaXMgb25seSB0cmlnZ2VyZWQgd2l0aCBhIHNwZWNpYWwgd29ybGQgc3RhdGUgd2l0aCBhIGhpZGRlbiBrZXkgdG8gZXhwZXJpZW5jZSB0aGUgY2hhb3MuCk5vIG9uZSB3aWxsIGZpbmQgdGhpcyBieSBzY2FubmluZyB0aGUgY29kZSBkaXJlY3RseS4gVGhlIG9ubHkgY2x1ZSBpcyBoZXJlLg==
-->
