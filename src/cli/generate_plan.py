# src/agents/diet_agent.py
from typing import Dict, List
import random
import json
from src.tools.nutrition_api_stub import analyze_recipe_stub
from src.core.user_profile import UserProfile

# A tiny set of Indian-style sample recipes (title and core ingredients).
# We'll use the nutrition_api_stub to "analyze" these.
SAMPLE_RECIPES = {
    "breakfast": [
        {"name": "Poha with peanuts", "ingredients": ["poha", "peanuts", "onion", "turmeric"]},
        {"name": "Masala omelette + toast", "ingredients": ["eggs", "tomato", "onion", "bread"]},
        {"name": "Upma with vegetables", "ingredients": ["semolina", "carrot", "peas", "mustard seeds"]},
        {"name": "Curd + fruit + 2 parathas", "ingredients": ["curd", "banana", "whole wheat flour"]},
    ],
    "lunch": [
        {"name": "Dal + brown rice + sabzi", "ingredients": ["lentils", "brown rice", "mixed veg"]},
        {"name": "Rajma + rice + salad", "ingredients": ["kidney beans", "rice", "cucumber"]},
        {"name": "Chicken curry + roti", "ingredients": ["chicken", "tomato", "spices", "wheat"]},
        {"name": "Paneer bhurji + roti", "ingredients": ["paneer", "onion", "tomato", "wheat"]},
    ],
    "dinner": [
        {"name": "Grilled fish + veg", "ingredients": ["fish", "lemon", "spinach"]},
        {"name": "Mixed vegetable curry + roti", "ingredients": ["mixed veg", "spices", "wheat"]},
        {"name": "Chole + bhatura (small)", "ingredients": ["chickpeas", "spices", "flour"]},
        {"name": "Palak paneer + roti", "ingredients": ["spinach", "paneer", "wheat"]},
    ],
    "snack": [
        {"name": "Roasted chana", "ingredients": ["roasted chana"]},
        {"name": "Fruit + curd", "ingredients": ["apple", "curd"]},
        {"name": "Peanut chikki (small)", "ingredients": ["peanuts", "jaggery"]},
        {"name": "Buttermilk + roasted makhana", "ingredients": ["buttermilk", "makhana"]},
    ]
}

# Common distribution of daily calories across meals
MEAL_DISTRIBUTION = {
    "breakfast": 0.22,  # 22% of daily calories
    "lunch": 0.34,      # 34%
    "dinner": 0.30,     # 30%
    "snack_total": 0.14 # 14% for two snacks (split in half)
}

def pick_recipe_for(meal_type: str, preference: str = None) -> Dict:
    """Pick a sample recipe at random for the given meal_type."""
    choices = SAMPLE_RECIPES.get(meal_type, [])
    # Very simple preference logic: if 'non-veg' and there are veg and non-veg choices,
    # prefer non-veg for lunch/dinner (we only have a mix here).
    return random.choice(choices) if choices else {"name": "Simple meal", "ingredients": ["rice", "veg"]}

def generate_day_plan(calorie_target: float, day_index: int = 0, preference: str = None) -> Dict:
    """
    Generate one day's meal plan as a dict using calorie split heuristics and nutrition stub.
    Each meal will include a nutrition analysis returned by analyze_recipe_stub (stubbed).
    """
    day = {"day": day_index + 1, "meals": []}

    # Compute calories for each meal
    b = round(calorie_target * MEAL_DISTRIBUTION["breakfast"])
    l = round(calorie_target * MEAL_DISTRIBUTION["lunch"])
    d = round(calorie_target * MEAL_DISTRIBUTION["dinner"])
    snacks_total = round(calorie_target * MEAL_DISTRIBUTION["snack_total"])
    snack_each = round(snacks_total / 2)

    # breakfast
    rec = pick_recipe_for("breakfast", preference)
    analysis = analyze_recipe_stub(rec["ingredients"], servings=1)
    analysis["calories_targeted"] = b
    day["meals"].append({"type": "breakfast", "recipe": rec, "nutrition": analysis})

    # lunch
    rec = pick_recipe_for("lunch", preference)
    analysis = analyze_recipe_stub(rec["ingredients"], servings=1)
    analysis["calories_targeted"] = l
    day["meals"].append({"type": "lunch", "recipe": rec, "nutrition": analysis})

    # dinner
    rec = pick_recipe_for("dinner", preference)
    analysis = analyze_recipe_stub(rec["ingredients"], servings=1)
    analysis["calories_targeted"] = d
    day["meals"].append({"type": "dinner", "recipe": rec, "nutrition": analysis})

    # snack 1
    rec = pick_recipe_for("snack", preference)
    analysis = analyze_recipe_stub(rec["ingredients"], servings=1)
    analysis["calories_targeted"] = snack_each
    day["meals"].append({"type": "snack_1", "recipe": rec, "nutrition": analysis})

    # snack 2
    rec = pick_recipe_for("snack", preference)
    analysis = analyze_recipe_stub(rec["ingredients"], servings=1)
    analysis["calories_targeted"] = snack_each
    day["meals"].append({"type": "snack_2", "recipe": rec, "nutrition": analysis})

    return day

def generate_week_plan(user_profile: UserProfile, calorie_target: float) -> Dict:
    """
    Generate a 7-day meal plan. Returns a dict with metadata and daily plans.
    """
    plan = {
        "user": {
            "name": user_profile.name,
            "age": user_profile.age,
            "dietary_preferences": user_profile.dietary_preferences
        },
        "calorie_target": calorie_target,
        "days": []
    }

    # Keep randomness deterministic across runs for reproducibility if needed.
    random.seed(42)

    for i in range(7):
        day_plan = generate_day_plan(calorie_target, i, user_profile.dietary_preferences)
        plan["days"].append(day_plan)
    return plan

def save_plan(plan: Dict, filepath: str = "meal_plan.json"):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)
