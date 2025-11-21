# src/tools/nutrition_api_stub.py
"""
A lightweight stub for nutrition API integration.
When you integrate a real API (Spoonacular/Edamam), replace these functions.
This allows you to run and test the agent locally without API keys.
"""

def analyze_recipe_stub(ingredients: list, servings=1):
    """
    Return a fake nutrition analysis (per-serving) for a list of ingredients.
    This is only for local development.
    """
    # Simple heuristic: 200 kcal per main meal per serving, 150 per snack.
    # Not accurate — replace with real API later.
    text = " + ".join(ingredients[:3])
    return {
        "title": f"Sample recipe: {text}",
        "calories_per_serving": 400 / max(1, servings),
        "protein_g": 25,
        "fat_g": 12,
        "carbs_g": 45
    }
