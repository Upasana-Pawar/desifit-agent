# tests/test_meal_plan.py
import json
from src.core.user_profile import UserProfile
from src.agents.diet_agent import generate_week_plan

def test_generate_week_plan_structure():
    profile = UserProfile(
        name="Test",
        age=30,
        sex="female",
        height_cm=160.0,
        weight_kg=60.0,
        activity_level="light",
        goal="lose_weight",
        target_rate_kg_per_week=0.5,
        dietary_preferences="vegetarian"
    )
    calorie_target = 1600
    plan = generate_week_plan(profile, calorie_target)
    assert "days" in plan and len(plan["days"]) == 7
    day0 = plan["days"][0]
    assert "meals" in day0 and len(day0["meals"]) == 5
    # check for expected meal types
    types = [m["type"] for m in day0["meals"]]
    assert "breakfast" in types and "lunch" in types and "dinner" in types
