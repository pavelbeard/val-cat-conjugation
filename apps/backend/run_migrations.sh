#!/bin/bash

# Set the PYTHONPATH to include the backend directory
export PYTHONPATH="/Users/pavelbeard/Documents/VSProjects/val-cat-conjugation/apps/backend:$PYTHONPATH"

# Change to the backend directory
cd "/Users/pavelbeard/Documents/VSProjects/val-cat-conjugation/apps/backend"

# Run the migration script
python run_migrations.py "$@"
