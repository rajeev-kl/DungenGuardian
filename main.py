import sys

from agent import DungeonGuardianAgent
from environment import DungeonEnvironment
from training import run_episode
from utils import print_banner

# Entry point for Dungeon Guardian Agent project


def interactive_mode():
    print_banner()
    env = DungeonEnvironment()
    agent = DungeonGuardianAgent()
    print("\nWelcome to the Dungeon Guardian Interactive Simulator!")
    print("Enter scenario values as prompted, or type 'exit' to quit.")
    while True:
        try:
            print("\n--- New Scenario ---")

            def get_val(prompt, cast, default):
                val = input(f"{prompt} (default {default}): ")
                if val.strip().lower() == "exit":
                    raise KeyboardInterrupt
                return cast(val) if val.strip() else default

            health = get_val("Health [0-100]", int, 50)
            stamina = get_val("Stamina [0-20]", int, 10)
            potion = get_val(
                "Has potion? [y/n]",
                lambda v: v.strip().lower() in ["y", "yes", "1"],
                False,
            )
            treasure = get_val("Treasure threat level [low/medium/high]", str, "medium")
            enemy = get_val(
                "Enemy nearby? [y/n]",
                lambda v: v.strip().lower() in ["y", "yes", "1"],
                False,
            )
            safe = get_val(
                "In safe zone? [y/n]",
                lambda v: v.strip().lower() in ["y", "yes", "1"],
                False,
            )
            world_state = {
                "health": health,
                "stamina": stamina,
                "hasPotion": potion,
                "treasureThreatLevel": treasure,
                "enemyNearby": enemy,
                "inSafeZone": safe,
            }
            run_episode(env, agent, world_state=world_state)
        except KeyboardInterrupt:
            print("\nExiting interactive mode. Goodbye!")
            break


def run_scenarios_from_json(json_path):
    import json

    print_banner()
    env = DungeonEnvironment()
    agent = DungeonGuardianAgent()
    print(f"\nLoading scenarios from {json_path} ...")
    with open(json_path, "r", encoding="utf-8") as f:
        scenarios = json.load(f)
    output_buffer = []
    for i, scenario in enumerate(scenarios, 1):
        scenario_output = f"\n=== Scenario {i} ===\n"
        print(scenario_output, end="")
        output_buffer.append(scenario_output)
        from io import StringIO

        temp_stdout = StringIO()
        sys_stdout = sys.stdout
        sys.stdout = temp_stdout
        run_episode(env, agent, world_state=scenario)
        sys.stdout = sys_stdout
        episode_output = temp_stdout.getvalue()
        print(episode_output, end="")
        output_buffer.append(episode_output)
    full_output = "".join(output_buffer)
    # Copy to clipboard (Linux/xclip)
    try:
        import subprocess

        subprocess.run("xclip -selection clipboard", input=full_output.encode(), shell=True, check=False)
        print("\n[INFO] Output copied to clipboard. Paste it into Copilot Chat in VS Code.")
    except (OSError, subprocess.CalledProcessError):
        print("\n[INFO] To get Copilot reasoning, copy the above output and paste it into Copilot Chat in VS Code.")


def copilot_special_mode():
    import json

    print_banner()
    scenario_path = "hell_mode_scenario.json"
    with open(scenario_path, "r", encoding="utf-8") as f:
        scenarios = json.load(f)
    env = DungeonEnvironment()
    agent = DungeonGuardianAgent()
    output_buffer = []
    for i, scenario in enumerate(scenarios, 1):
        scenario_output = f"\n=== Scenario {i} ===\n"
        print(scenario_output, end="")
        output_buffer.append(scenario_output)
        from io import StringIO

        temp_stdout = StringIO()
        sys_stdout = sys.stdout
        sys.stdout = temp_stdout
        run_episode(env, agent, world_state=scenario)
        sys.stdout = sys_stdout
        episode_output = temp_stdout.getvalue()
        print(episode_output, end="")
        output_buffer.append(episode_output)
    full_output = "".join(output_buffer)
    # Copy to clipboard (Linux/xclip)
    try:
        import subprocess

        subprocess.run("xclip -selection clipboard", input=full_output.encode(), shell=True, check=False)
        print("\n[INFO] Output copied to clipboard. Paste it into Copilot Chat in VS Code.")
    except (OSError, subprocess.CalledProcessError):
        print("\n[INFO] To get Copilot reasoning, copy the above output and paste it into Copilot Chat in VS Code.")


def main():
    args = sys.argv[1:]
    if args:
        if args[0] == "--interactive":
            interactive_mode()
            return
        elif args[0].endswith(".json"):
            run_scenarios_from_json(args[0])
            return
    print_banner()
    env = DungeonEnvironment()
    agent = DungeonGuardianAgent()
    output_buffer = []
    # Scenario 1: Low Health, No Healing Resources, Enemy Nearby
    scenario1 = {
        "health": 20,
        "enemyNearby": True,
        "hasPotion": False,
        "treasureThreatLevel": "medium",
        "stamina": 5,
        "inSafeZone": False,
    }
    scenario_output = "\n=== Scenario 1: Low Health, No Healing Resources, Enemy Nearby ===\n"
    print(scenario_output, end="")
    output_buffer.append(scenario_output)
    from io import StringIO

    temp_stdout = StringIO()
    sys_stdout = sys.stdout
    sys.stdout = temp_stdout
    run_episode(env, agent, world_state=scenario1)
    sys.stdout = sys_stdout
    episode_output = temp_stdout.getvalue()
    print(episode_output, end="")
    output_buffer.append(episode_output)
    # Scenario 2: Healthy, Treasure Under Threat, Enemy Nearby
    scenario2 = {
        "health": 85,
        "enemyNearby": True,
        "hasPotion": True,
        "treasureThreatLevel": "high",
        "stamina": 15,
        "inSafeZone": False,
    }
    scenario_output = "\n=== Scenario 2: Healthy, Treasure Under Threat, Enemy Nearby ===\n"
    print(scenario_output, end="")
    output_buffer.append(scenario_output)
    temp_stdout = StringIO()
    sys.stdout = temp_stdout
    run_episode(env, agent, world_state=scenario2)
    sys.stdout = sys_stdout
    episode_output = temp_stdout.getvalue()
    print(episode_output, end="")
    output_buffer.append(episode_output)
    # Scenario 3: No Enemy Nearby, Low Stamina, Potion Available
    scenario3 = {
        "health": 70,
        "enemyNearby": False,
        "hasPotion": True,
        "treasureThreatLevel": "low",
        "stamina": 2,
        "inSafeZone": True,
    }
    scenario_output = "\n=== Scenario 3: No Enemy Nearby, Low Stamina, Potion Available ===\n"
    print(scenario_output, end="")
    output_buffer.append(scenario_output)
    temp_stdout = StringIO()
    sys.stdout = temp_stdout
    run_episode(env, agent, world_state=scenario3)
    sys.stdout = sys_stdout
    episode_output = temp_stdout.getvalue()
    print(episode_output, end="")
    output_buffer.append(episode_output)
    # Scenario 4: Out of Potions, Enemy Near, Treasure Safe
    scenario4 = {
        "health": 60,
        "enemyNearby": True,
        "hasPotion": False,
        "treasureThreatLevel": "low",
        "stamina": 10,
        "inSafeZone": False,
    }
    scenario_output = "\n=== Scenario 4: Out of Potions, Enemy Near, Treasure Safe ===\n"
    print(scenario_output, end="")
    output_buffer.append(scenario_output)
    temp_stdout = StringIO()
    sys.stdout = temp_stdout
    run_episode(env, agent, world_state=scenario4)
    sys.stdout = sys_stdout
    episode_output = temp_stdout.getvalue()
    print(episode_output, end="")
    output_buffer.append(episode_output)
    full_output = "".join(output_buffer)
    # Copy to clipboard (Linux/xclip)
    try:
        import subprocess

        subprocess.run("xclip -selection clipboard", input=full_output.encode(), shell=True, check=False)
        print("\n[INFO] Output copied to clipboard. Paste it into Copilot Chat in VS Code.")
    except (OSError, subprocess.CalledProcessError):
        print("\n[INFO] To get Copilot reasoning, copy the above output and paste it into Copilot Chat in VS Code.")


if __name__ == "__main__":
    main()
