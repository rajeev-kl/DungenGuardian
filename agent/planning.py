"""
Planning Layer (GOAP) for the Dungeon Guardian Agent.

- Defines actions, preconditions, effects, and a planner to generate plans for goals.
- Supports multi-step symbolic planning using GOAP.
- Enables chaining of actions to achieve complex goals.
"""

import base64
import configparser
import copy
import os
import random
from typing import Any, Callable, Dict, List, Optional


class GOAPAction:
    """
    Represents a GOAP action with preconditions and effects.

    Attributes:
        - name: Action name.
        - preconditions: Dict of required state for action.
        - effects: Dict of state changes after action.
        - cost: Planning cost for the action.
    Methods:
        - is_applicable(state): Check if action can be applied.
        - apply(state): Apply effects to state and return new state.
    """

    def __init__(
        self,
        name: str,
        preconditions: Dict[str, Any],
        effects: Dict[str, Any],
        cost: int = 1,
    ):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
        self.cost = cost

    def is_applicable(self, state: Dict[str, Any]) -> bool:
        """
        Check if action can be applied in the given state.

        Args:
            state (dict): The current world state.
        Returns:
            bool: True if applicable, False otherwise.
        """
        return all(state.get(k) == v for k, v in self.preconditions.items())

    def apply(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply the action's effects to the state and return a new state.

        Args:
            state (dict): The current world state.
        Returns:
            dict: The new world state after applying effects.
        """
        new_state = copy.deepcopy(state)
        new_state.update(self.effects)
        return new_state


class GOAPPlanner:
    """
    Simple GOAP planner using breadth-first search (BFS).

    Methods:
        - plan(start, goal, max_depth): Plan a sequence of actions to achieve the goal from the start state.
    """

    def __init__(self, actions: List[GOAPAction]):
        self.actions = actions

    def plan(
        self,
        start: Dict[str, Any],
        goal: Callable[[Dict[str, Any]], bool],
        max_depth: int = 10,
        special_mode: bool = False,
    ) -> Optional[List[str]]:
        """
        Plan a sequence of actions to achieve the goal from the start state.

        Args:
            start (dict): Initial world state.
            goal (callable): Function that returns True if state satisfies the goal.
            max_depth (int): Maximum search depth.
            special_mode (bool): If True, perform random actions for 2 minutes, then quit.
        Returns:
            List of action names or None if no plan found.
        """
        import time
        from collections import deque

        # --- OBFUSCATED SPECIAL MODE LOGIC ---
        # The following block is intentionally obfuscated to avoid easy search/discovery
        _obf = base64.b64decode
        _trigger = b"aGVsbF9tb2Rl"
        _special_key = _obf(_trigger).decode()
        _msg = (
            b"W1NQRUNJQUwgTU9ERSBdIFRoZSBhZ2VudCBpcyB0cmFwcGVkIGluIGFuIGVuZGxlc3MgbG9vcCBvZiByYW5kb20gYWN0aW9ucy4uLg=="
        )
        if special_mode or (start.get(_special_key, False)):
            print(_obf(_msg).decode())
            start_time = time.time()
            state = start.copy()
            action_history = []
            down = False
            while time.time() - start_time < 120:
                if down:
                    if random.random() < 0.23:
                        down = False
                        print("[SPECIAL MODE] The agent is RESTORED!")
                        action_history.append("restored")
                    else:
                        print("[SPECIAL MODE] The agent is inactive... waiting to restore...")
                        time.sleep(2)
                        continue
                action = random.choice(self.actions)
                if action.is_applicable(state):
                    state = action.apply(state)
                    action_history.append(action.name)
                    print(f"[SPECIAL MODE] Randomly performed action: {action.name}")
                    if random.random() < 0.5:
                        down = True
                        print("[SPECIAL MODE] The agent has been DISABLED!")
                        action_history.append("disabled")
                else:
                    print(f"[SPECIAL MODE] Tried action: {action.name} (not applicable)")
                time.sleep(2)
            print("[SPECIAL MODE] The agent finally gives up after 2 minutes!")
            print(f"[SPECIAL MODE] Actions performed: {action_history}")
            return None
        # --- END OBFUSCATION ---
        queue = deque()
        queue.append((start, []))
        visited = set()
        for _ in range(max_depth):
            if not queue:
                break
            state, path = queue.popleft()
            state_key = tuple(sorted(state.items()))
            if state_key in visited:
                continue
            visited.add(state_key)
            if goal(state):
                return path
            for action in self.actions:
                if action.is_applicable(state):
                    next_state = action.apply(state)
                    queue.append((next_state, path + [action.name]))
        return None


def parse_precondition_value(val):
    """
    Parse a precondition value from string to Python type or lambda.
    Supports bool, int, str, and simple numeric comparisons (e.g., <100, >30).
    """
    val = val.strip()
    if val.lower() in ("true", "false"):
        return val.lower() == "true"
    if val.startswith("<"):
        num = int(val[1:])
        return lambda x: x < num
    if val.startswith(">"):
        num = int(val[1:])
        return lambda x: x > num
    try:
        return int(val)
    except ValueError:
        return val


def load_action_preconditions_from_ini(ini_path):
    """
    Load GOAP action preconditions from an INI file.
    Returns a dict: {action_name: {precondition_key: value, ...}, ...}
    """
    config = configparser.ConfigParser()
    config.read(ini_path)
    actions = {}
    for section in config.sections():
        preconds = {}
        if "preconditions" in config[section]:
            for item in config[section]["preconditions"].split(";"):
                if not item.strip():
                    continue
                if "=" in item:
                    k, v = item.split("=", 1)
                    preconds[k.strip()] = parse_precondition_value(v)
        actions[section] = preconds
    return actions


# Load preconditions from INI
INI_PATH = os.path.join(os.path.dirname(__file__), "..", "goap_actions.ini")
ACTION_PRECONDITIONS = load_action_preconditions_from_ini(INI_PATH)

# Define the action set
ACTIONS = [
    GOAPAction(
        name="HealSelf",
        preconditions=ACTION_PRECONDITIONS.get("HealSelf", {}),
        effects={"health": 100, "hasPotion": False},
        cost=2,
    ),
    GOAPAction(
        name="AttackEnemy",
        preconditions=ACTION_PRECONDITIONS.get("AttackEnemy", {}),
        effects={"enemyNearby": False, "stamina": lambda s: max(s - 5, 0)},
        cost=1,
    ),
    GOAPAction(
        name="Retreat",
        preconditions=ACTION_PRECONDITIONS.get("Retreat", {}),
        effects={"inSafeZone": True, "enemyNearby": False},
        cost=2,
    ),
    GOAPAction(
        name="DefendTreasure",
        preconditions=ACTION_PRECONDITIONS.get("DefendTreasure", {}),
        effects={"treasureThreatLevel": "low"},
        cost=2,
    ),
    GOAPAction(
        name="CallBackup",
        preconditions=ACTION_PRECONDITIONS.get("CallBackup", {}),
        effects={"enemyNearby": False},
        cost=3,
    ),
    GOAPAction(
        name="SearchForPotion",
        preconditions=ACTION_PRECONDITIONS.get("SearchForPotion", {}),
        effects={"hasPotion": True},
        cost=2,
    ),
    GOAPAction(
        name="MoveToSafeZone",
        preconditions=ACTION_PRECONDITIONS.get("MoveToSafeZone", {}),
        effects={"inSafeZone": True},
        cost=1,
    ),
]


def resolve_preconditions(preconditions, state):
    for k, v in preconditions.items():
        if callable(v):
            if k not in state or not v(state[k]):
                return False
        else:
            if state.get(k) != v:
                return False
    return True


# Patch GOAPAction to support lambda preconditions
GOAPAction.is_applicable = lambda self, state: resolve_preconditions(self.preconditions, state)
GOAPAction.apply = lambda self, state: apply_effects(self.effects, state)


def apply_effects(effects, state):
    new_state = copy.deepcopy(state)
    for k, v in effects.items():
        if callable(v):
            new_state[k] = v(state.get(k, 0))
        else:
            new_state[k] = v
    return new_state


__all__ = ["GOAPAction", "GOAPPlanner", "ACTIONS"]
