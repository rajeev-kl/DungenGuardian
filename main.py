import subprocess
import json
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

        subprocess.run("xclip -selection clipboard", input=full_output.encode(), shell=True, check=False)
        print("\n[INFO] Output copied to clipboard. Paste it into Copilot Chat in VS Code.")
    except (OSError, subprocess.CalledProcessError):
        print("\n[INFO] To get Copilot reasoning, copy the above output and paste it into Copilot Chat in VS Code.")


def show_help():
    print_banner()
    print(
        """
Usage: python main.py [interactive|<scenarios.json>]

Modes:
  interactive         Run the agent in interactive mode (enter scenarios by hand)
  <scenarios.json>    Run the agent on a batch of scenarios from a JSON file

Examples:
  python main.py interactive
  python main.py true_multistep_scenarios.json

After batch runs, output is copied to your clipboard (Linux/xclip required) for easy Copilot Chat use in VS Code.
"""
    )


def main():
    args = sys.argv[1:]
    if args:
        if args[0] == "interactive":
            interactive_mode()
            return
        elif args[0].endswith(".json"):
            run_scenarios_from_json(args[0])
            return
    show_help()


if __name__ == "__main__":
    main()
