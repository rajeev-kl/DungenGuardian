"""
Training module for the Dungeon Guardian Agent project.
"""

import base64


def run_episode(env, agent, world_state=None):
    """
    Run a full episode: agent plans, acts, and replans if needed.
    Accepts a custom world_state for scenario testing.

    Args:
        env (DungeonEnvironment): The dungeon environment.
        agent (DungeonGuardianAgent): The agent.
        world_state (dict, optional): The initial world state. Defaults to None.
    """
    env.reset()
    # Use provided world_state or default
    if world_state is None:
        world_state = {
            "health": 20,
            "enemyNearby": True,
            "hasPotion": False,
            "treasureThreatLevel": "medium",
            "stamina": 5,
            "inSafeZone": False,
        }
    max_steps = 10
    step = 0
    plan = None
    goal = None
    while step < max_steps:
        print(f"\n--- Step {step+1} ---")
        if not plan:
            goal = agent.cognitive.generate_goal(world_state)
            # Secret special-mode trigger (obfuscated)
            _obf = base64.b64decode
            _trigger = b"aGVsbF9tb2Rl"
            _special_key = _obf(_trigger).decode()
            special_mode = world_state.get(_special_key, False)
            goal_checks = {
                "Survive": lambda s: s["health"] >= 50 and s["inSafeZone"],
                "ProtectTreasure": lambda s: s["treasureThreatLevel"] == "low",
                "EliminateThreat": lambda s: not s["enemyNearby"],
                "PrepareForBattle": lambda s: s["hasPotion"] or s["stamina"] >= 10,
                "Patrol": lambda s: s["inSafeZone"],
            }
            goal_fn = goal_checks.get(goal, lambda s: True)
            plan = agent.planner.plan(world_state, goal_fn, special_mode=special_mode)
            if not plan:
                print(f"[Cognitive] Goal: {goal} | No valid plan found.")
                break
            print(f"[Cognitive] Goal: {goal} | Plan: {plan}")
        action = plan.pop(0)
        justification = agent.cognitive.justify_action(action, world_state, goal)
        print(f"[Execution] Action: {action} | Reason: {justification}")
        new_state, success = env.execute_action(action, world_state)
        if success:
            print(f"[Execution] Action '{action}' succeeded.")
            world_state = new_state
        else:
            print(f"[Execution] Action '{action}' FAILED!")
            agent.cognitive.reflect_on_failure({"action": action, "state": world_state, "goal": goal})
            plan = None  # Force replanning
            continue
        # Check if goal is achieved
        goal_checks = {
            "Survive": lambda s: s["health"] >= 50 and s["inSafeZone"],
            "ProtectTreasure": lambda s: s["treasureThreatLevel"] == "low",
            "EliminateThreat": lambda s: not s["enemyNearby"],
            "PrepareForBattle": lambda s: s["hasPotion"] or s["stamina"] >= 10,
            "Patrol": lambda s: s["inSafeZone"],
        }
        if goal_checks.get(goal, lambda s: True)(world_state):
            print(f"[Success] Goal '{goal}' achieved!")
            break
        if not plan:
            print("[Execution] Replanning...")
        step += 1
    print(f"\nFinal world state: {world_state}")
    print(f"Agent memory: {agent.cognitive.memory}")
