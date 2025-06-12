"""
Cognitive Layer for the Dungeon Guardian Agent.

- Handles goal generation, reflection, and action justification.
- Simulates LLM-style reasoning for the agent.
- Maintains a memory of failures and choices.
"""

from typing import Any, Dict, List


class CognitiveEngine:
    """
    Simulates LLM-style reasoning for the agent.

    Methods:
        - generate_goal(world_state): Generate a goal from the current world state.
        - reflect_on_failure(failure): Update memory with failed plans/actions.
        - justify_action(action, world_state, goal): Explain the chosen action in natural language.
    """

    def __init__(self):
        self.memory: List[Dict[str, Any]] = []  # Stores past failures, choices, outcomes

    def generate_goal(self, world_state: Dict[str, Any]) -> str:
        """
        Generate a goal based on the current world state.

        Args:
            world_state (dict): The current state of the world.
        Returns:
            str: The chosen goal.
        """
        # Heuristic goal selection (can be replaced with LLM call)
        if world_state["health"] < 30:
            return "Survive"
        if world_state["treasureThreatLevel"] == "high":
            return "ProtectTreasure"
        if world_state["enemyNearby"]:
            return "EliminateThreat"
        if world_state["stamina"] < 5:
            return "PrepareForBattle"
        return "Patrol"

    def reflect_on_failure(self, failure: Dict[str, Any]):
        """
        Reflect on a failed plan or action and update memory.

        Args:
            failure (dict): Information about the failure.
        """
        self.memory.append(failure)

    def justify_action(self, action: str, world_state: Dict[str, Any], goal: str) -> str:
        """
        Provide a natural language justification for the chosen action.

        Args:
            action (str): The action taken.
            world_state (dict): The current state of the world.
            goal (str): The current goal.
        Returns:
            str: Natural language explanation.
        """
        if action == "HealSelf":
            if not world_state.get("hasPotion", False):
                return "I wanted to heal, but I have no potions."
            return "I chose to heal because my health is low."
        if action == "Retreat":
            return "I chose to retreat because survival is my top priority."
        if action == "AttackEnemy":
            return "I chose to attack because the enemy is nearby and my health is sufficient."
        if action == "DefendTreasure":
            return "I am defending the treasure because its threat level is high."
        if action == "CallBackup":
            return "I called for backup due to overwhelming threats."
        if action == "SearchForPotion":
            return "I am searching for a potion to prepare for future threats."
        if action == "MoveToSafeZone":
            return "I am moving to a safe zone to increase my chances of survival."
        return f"I chose to {action} to achieve my goal: {goal}."
