"""
Dungeon environment module for the Dungeon Guardian Agent project.

- Simulates the dungeon environment for the agent.
- Provides methods to reset and render the environment.
- Handles action execution, simulating success/failure and updating world state.
"""


class DungeonEnvironment:
    """
    Represents the dungeon environment where the agent operates.

    Methods:
        - reset(): Reset the environment to the initial state.
        - render(): Print a simple representation of the dungeon.
        - execute_action(action, state): Simulate action execution, update state, and return (new_state, success).
    """

    def __init__(self, width=5, height=5):
        """
        Initialize the dungeon environment.

        Args:
            width (int): Width of the dungeon grid.
            height (int): Height of the dungeon grid.
        """
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        # 0: empty, 1: wall, 2: intruder, 3: agent

    def reset(self):
        """
        Reset the environment to the initial state.
        """
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def render(self):
        """
        Print a simple representation of the dungeon.
        """
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

    def execute_action(self, action: str, state: dict) -> tuple:
        """
        Simulate the execution of an action, update the state, and return (new_state, success).

        Args:
            action (str): The action to execute.
            state (dict): The current world state.
        Returns:
            (dict, bool): The new state and whether the action succeeded.
        """
        import random

        # Simulate possible failure for some actions
        fail_chance = {
            "HealSelf": 0.2,  # 20% chance potion is spoiled/stolen
            "AttackEnemy": 0.1,
            "Retreat": 0.05,
            "DefendTreasure": 0.05,
            "CallBackup": 0.1,
            "SearchForPotion": 0.15,
        }
        success = random.random() > fail_chance.get(action, 0)
        # Only update state if action succeeded
        if success:
            from agent.planning import ACTIONS

            act = next((a for a in ACTIONS if a.name == action), None)
            if act:
                # Use patched apply to handle lambdas
                new_state = act.apply(state)
                return new_state, True
        return state, False
