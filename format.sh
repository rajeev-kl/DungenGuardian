#!/bin/bash
# Format and lint the Dungeon Guardian Agent project

set -e

# Run isort
isort .

# Run black
black .

# Run flake8
flake8 .

echo "\n[INFO] Formatting and linting complete."
