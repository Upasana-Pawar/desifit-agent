# src/agents/diet_agent.py
"""
Diet agent for DesiFit (Day 2).
Provides functions to generate a 7-day Indian-aware meal plan using a local stub for nutrition analysis.
Replace `analyze_recipe_stub` with a real API call (Spoonacular / Edamam) later.

Key functions:
- generate_day_plan(calorie_target, day_index, preference)
- generate_week_plan(user_profile, calorie_target)
- generate_weekly_plan(...)  <- alias used by tests
- save_plan(plan, filepath="meal_plan.json")
- generate_and_save_plan(user_profile, calorie_target, filepath="meal_plan.json")
"""

from typing import Dict, List, Optional
import random
import json
from src.tools.nutrition_api_stub import analyze_recipe_stub
from src.core.user_profile import UserProfile

# ---------- Sample recipes ----------
# Small curated list of Indian-style sample recipes.
# Each recipe has a 'tags' list marking if it's 'veg' or 'non-veg' for simple preference filtering.
SAMPLE_RECIPES = {
    "breakfast": [
        {"name": "Poha with peanuts", "ingredients": ["poha", "peanuts", "onion", "turmeric"], "tags": ["veg"]},
        {"name": "Masala omelette + toast", "ingredients": ["eggs", "tomato", "onion", "bread"], "tags": ["non-veg"]},
        {"name": "Upma with vegetables", "ingredients": ["semolina", "carrot", "peas", "mustard seeds"], "tags": ["veg"]},
        {"name": "Curd + fruit + 2 parathas", "ingredients": ["curd", "banana", "whole wheat flour"], "tags": ["veg"]},
    ],
    "lunch": [
        {"name": "Dal + brown rice + sabzi", "ingredients": ["lentils", "brown rice", "mixed veg"], "tags": ["veg"]},
        {"name": "Rajma + rice + salad", "ingredients": ["kidney beans", "rice", "cucumber"], "tags": ["veg"]},
        {"name": "Chicken curry + roti", "ingredients": ["chicken", "tomato", "spices", "wheat"], "tags": ["non-veg"]},
        {"name": "Paneer bhurji + roti", "ingredients": ["paneer", "onion", "tomato", "wheat"], "tags": ["veg"]},
    ],
    "dinner": [
        {"name": "Grilled fish + veg", "ingredients": ["fish", "lemon", "spinach"], "tags": ["non-veg"]},
        {"name": "Mixed vegetable curry + roti", "ingredients": ["mixed veg", "spices", "wheat"], "tags": ["veg"]},
        {"name": "Chole + bhatura (small)", "ingredients": ["chickpeas", "spices", "flour"], "tags": ["veg"]},
        {"name": "Palak paneer + roti", "ingredients": ["spinach", "paneer", "wheat"], "tags": ["veg"]},
    ],
    "snack": [
        {"name": "Roasted chana", "ingredients": ["roasted chana"], "tags": ["veg"]},
        {"name": "Fruit + curd", "ingredients": ["apple", "curd"], "tags": ["veg"]},
        {"name": "Peanut chikki (small)", "ingredients": ["peanuts", "jaggery"], "tags": ["veg"]},
        {"name": "Buttermilk + roasted makhana", "ingredients": ["buttermilk", "makhana"], "tags": ["veg"]},
    ]
}

# Distribution of daily calories across meals
MEAL_DISTRIBUTION = {
    "breakfast": 0.22,   # 22% of daily calories
    "lunch": 0.34,       # 34%
    "dinner": 0.30,      # 30%
    "snack_total": 0.14  # 14% for two snacks
}

# Helper: filter recipes by preference string (very simple)
def _filter_by_preference(recipes: List[Dict], preference: Optional[str]) -> List[Dict]:
    if not preference:
        return recipes
    pref = preference.lower()
    # Example preferences: 'vegetarian', 'non-veg', 'vegan' (we only support veg/non-veg filtering here)
    if "veg" in pref:
        return [r for r in recipes if "veg" in r.get("tags", [])]
    if "non" in pref or "non-veg" in pref or "nonveg" in pref:
        return [r for r in recipes if "non-veg" in r.get("tags", [])]
    # fallback: return original list
    return recipes

def pick_recipe_for(meal_type: str, preference: Optional[str] = None) -> Dict:
    """Pick a recipe (random) for a meal_type while applying preference filters."""
    choices = SAMPLE_RECIPES.get(meal_type, [])
    filtered = _filter_by_preference(choices, preference)
    final_choices = filtered if filtered else choices
    if not final_choices:
        # fallback generic meal
        return {"name": "Simple meal", "ingredients": ["rice", "veg"], "tags": ["veg"]}
    return random.choice(final_choices)

def generate_day_plan(calorie_target: float, day_index: int = 0, preference: Optional[str] = None) -> Dict:
    """
    Generate one day's meal plan:
    - Uses MEAL_DISTRIBUTION to split calories to meals/snacks.
    - Uses analyze_recipe_stub(...) to get a nutrition stub per chosen recipe.
    - Adds a 'calories_targeted' field per meal so downstream code can tune portion sizes.
    """
    day = {"day": day_index + 1, "meals": []}

    # Compute calories per meal
    b = round(calorie_target * MEAL_DISTRIBUTION["breakfast"])
    l = round(calorie_target * MEAL_DISTRIBUTION["lunch"])
    d = round(calorie_target * MEAL_DISTRIBUTION["dinner"])
    snacks_total = round(calorie_target * MEAL_DISTRIBUTION["snack_total"])
    snack_each = round(snacks_total / 2)

    # Breakfast
    rec = pick_recipe_for("breakfast", preference)
    analysis = analyze_recipe_stub(rec["ingredients"], servings=1)
    analysis["calories_targeted"] = b
    day["meals"].append({"type": "breakfast", "recipe": rec, "nutrition": analysis})

    # Lunch
    rec = pick_recipe_for("lunch", preference)
    analysis = analyze_recipe_stub(rec["ingredients"], servings=1)
    analysis["calories_targeted"] = l
    day["meals"].append({"type": "lunch", "recipe": rec, "nutrition": analysis})

    # Dinner
    rec = pick_recipe_for("dinner", preference)
    analysis = analyze_recipe_stub(rec["ingredients"], servings=1)
    analysis["calories_targeted"] = d
    day["meals"].append({"type": "dinner", "recipe": rec, "nutrition": analysis})

    # Snack 1
    rec = pick_recipe_for("snack", preference)
    analysis = analyze_recipe_stub(rec["ingredients"], servings=1)
    analysis["calories_targeted"] = snack_each
    day["meals"].append({"type": "snack_1", "recipe": rec, "nutrition": analysis})

    # Snack 2
    rec = pick_recipe_for("snack", preference)
    analysis = analyze_recipe_stub(rec["ingredients"], servings=1)
    analysis["calories_targeted"] = snack_each
    day["meals"].append({"type": "snack_2", "recipe": rec, "nutrition": analysis})

    return day

def generate_week_plan(user_profile: UserProfile, calorie_target: float, seed: int = 42) -> Dict:
    """
    Generate a 7-day meal plan for the given user profile and calorie target.
    - Uses deterministic random seed by default for reproducible outputs (useful for tests).
    - Returns a dict with metadata and daily plans.
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
    random.seed(seed)
    for i in range(7):
        day_plan = generate_day_plan(calorie_target, i, user_profile.dietary_preferences)
        plan["days"].append(day_plan)
    return plan

# Alias expected by tests and external callers.
# Tests were importing `generate_weekly_plan`, so provide that name to avoid import errors.
generate_weekly_plan = generate_week_plan

def save_plan(plan: Dict, filepath: str = "meal_plan.json"):
    """Save the plan as JSON (pretty printed)."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)
    return filepath

def generate_and_save_plan(user_profile: UserProfile, calorie_target: float, filepath: str = "meal_plan.json") -> Dict:
    """
    Convenience helper: generate week plan and write to disk.
    Returns the plan dict (and writes file).
    """
    plan = generate_week_plan(user_profile, calorie_target)
    save_plan(plan, filepath)
    return plan

# If run as a script for quick manual testing:
if __name__ == "__main__":
    # Minimal demo (requires `session_profile.json` or create a short UserProfile object)
    try:
        # lazy import here to avoid circular import during tests if not present
        from src.core.user_profile import load_profile
        profile = load_profile()
        if not profile:
            # quick fallback demo profile
            profile = UserProfile(
                name="Demo",
                age=25,
                sex="female",
                height_cm=162.0,
                weight_kg=70.0,
                activity_level="light",
                goal="lose_weight",
                target_rate_kg_per_week=0.5,
                dietary_preferences="vegetarian"
            )
        # naive calorie target: use 2000 if not computed externally
        plan = generate_week_plan(profile, calorie_target=1800)
        save_plan(plan, "meal_plan.json")
        print("Saved weekly plan to meal_plan.json")
    except Exception as e:
        print("Error running demo:", e)
