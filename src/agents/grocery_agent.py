# src/agents/grocery_agent.py

"""
Grocery List Agent for DesiFit.
Generates a consolidated grocery list from the weekly meal_plan.json file.
"""

import json
from typing import Dict, List
from collections import defaultdict

def load_meal_plan(filepath: str = "meal_plan.json") -> Dict:
    """Load the weekly meal plan JSON."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_grocery_list(meal_plan: Dict) -> Dict[str, int]:
    """
    Extract all ingredients from the weekly meal plan
    and count occurrences (basic approximation).
    """
    grocery = defaultdict(int)

    for day in meal_plan["days"]:
        for meal in day["meals"]:
            ingredients = meal["recipe"]["ingredients"]
            for ingredient in ingredients:
                grocery[ingredient] += 1

    return dict(grocery)

def save_grocery_list(grocery: Dict[str, int], filepath: str = "grocery_list.json"):
    """Save grocery list to disk."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(grocery, f, indent=2)
    print(f"Saved grocery list to {filepath}")

def generate_and_save_grocery_list(meal_plan_path="meal_plan.json"):
    """Convenience function to load meal plan and save grocery list."""
    meal_plan = load_meal_plan(meal_plan_path)
    grocery = generate_grocery_list(meal_plan)
    save_grocery_list(grocery)
    return grocery


# For manual testing
if __name__ == "__main__":
    generate_and_save_grocery_list()
