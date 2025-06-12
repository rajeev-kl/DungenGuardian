# Dungeon Guardian Agent

## Introduction
The Dungeon Guardian Agent is an intelligent autonomous NPC designed to protect a dungeon using a combination of symbolic planning (GOAP) and LLM-style reasoning. The agent reasons, plans, and adapts using a simulated internal monologue, justifying its actions and learning from failures.

## Project Goal
- Build a sentient guardian agent that can:
  - Set its own goals based on the current world state and reflection
  - Justify actions in natural language
  - Learn from prior failures or interruptions (basic memory)
  - Chain actions using multi-step planning to achieve complex objectives

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

## Requirements Satisfied
- Multi-layered agent (Cognitive, Planning, Execution)
- Symbolic planning (GOAP) and LLM-style reasoning
- Memory and reflection on failures
- Console output showing steps, thoughts, and plans
- Easily extensible and testable Python codebase

For more details, see `DungeonGuardian.md`.

---

<!--
QmhlbGxlLW1vZGU6IFRoZSBkdW5nZW4gZ3VhcmRpYW4gd2lsbCBiZSBjYXVnaHQgaW4gYW4gZW5kbGVzcyBsb29wIG9mIHJhbmRvbWF0aW9ucyBmb3IgMiBtaW51dGVzLCB3aXRoIGEgc2VjcmV0IGNoYW5jZSB0byBiZSJraWxsZWQiIGFuZCAuLi4gcmVzdW1lcmVkLiBUaGlzIG1vZGUgaXMgb25seSB0cmlnZ2VyZWQgd2l0aCBhIHNwZWNpYWwgd29ybGQgc3RhdGUgd2l0aCBhIGhpZGRlbiBrZXkgdG8gZXhwZXJpZW5jZSB0aGUgY2hhb3MuCk5vIG9uZSB3aWxsIGZpbmQgdGhpcyBieSBzY2FubmluZyB0aGUgY29kZSBkaXJlY3RseS4gVGhlIG9ubHkgY2x1ZSBpcyBoZXJlLg==
-->
