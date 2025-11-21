# tests/test_diet_agent.py
from src.agents.diet_agent import generate_weekly_plan
from src.core.user_profile import UserProfile

def make_sample_profile():
    return UserProfile(
        name="Test",
        age=30,
        sex="female",
        height_cm=160.0,
        weight_kg=65.0,
        activity_level="light",
        goal="lose_weight",
        target_rate_kg_per_week=0.5,
        dietary_preferences="vegetarian"
    )

def test_generate_weekly_plan_structure():
    profile = make_sample_profile()
    # choose a sample calorie target
    plan = generate_weekly_plan(profile, calorie_target=1800)
    assert "user" in plan
    assert "calorie_target" in plan
    assert plan["calorie_target"] == 1800
    assert "days" in plan
    assert len(plan["days"]) == 7
    # each day should have a meals list
    for d in plan["days"]:
        assert "meals" in d
        assert len(d["meals"]) >= 4  # breakfast,lunch,dinner,2 snacks => minimum 4 entries
