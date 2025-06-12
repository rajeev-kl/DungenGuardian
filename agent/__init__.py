"""
Agent module for the Dungeon Guardian Agent project.
"""

from agent.planning import ACTIONS, GOAPPlanner

from .cognitive import CognitiveEngine


class DungeonGuardianAgent:
    """
    Represents the dungeon guardian agent.
    """

    def __init__(self, name="Guardian"):
        """
        Initialize the agent.
        Args:
            name (str): Name of the agent.
        """
        self.name = name
        self.cognitive = CognitiveEngine()
        self.planner = GOAPPlanner(ACTIONS)

    def act(self, world_state):
        """
        Decide on an action based on the observation.
        Args:
            world_state: The current state observation from the environment.
        Returns:
            action: The action to take.
        """
        goal = self.cognitive.generate_goal(world_state)
        # Map goal to a goal-checking function
        goal_checks = {
            "Survive": lambda s: s["health"] >= 50 or s["inSafeZone"],
            "ProtectTreasure": lambda s: s["treasureThreatLevel"] == "low",
            "EliminateThreat": lambda s: not s["enemyNearby"],
            "PrepareForBattle": lambda s: s["hasPotion"] or s["stamina"] >= 10,
            "Patrol": lambda s: s["inSafeZone"],
        }
        goal_fn = goal_checks.get(goal, lambda s: True)
        plan = self.planner.plan(world_state, goal_fn)
        if plan:
            action = plan[0]
            justification = self.cognitive.justify_action(action, world_state, goal)
            print(f"[Cognitive] Goal: {goal} | Plan: {plan} | Next Action: {action} | Reason: {justification}")
            return action
        else:
            print(f"[Cognitive] Goal: {goal} | No valid plan found.")
            return None
