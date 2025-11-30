# src/agents/coordinator.py
"""
Coordinator for DesiFit.

Responsibilities:
- Load user profile (from session_profile.json).
- Compute BMR, TDEE, calorie target, and macros.
- Call Diet Agent to generate + save 7-day meal plan.
- Call Workout Agent to generate + save weekly workout plan.
- Print a human-readable summary to the console.

This is the main entry point for the CLI demo.
"""
from src.agents.grocery_agent import generate_and_save_grocery_list

from dataclasses import asdict
from typing import Dict

from src.core.user_profile import load_profile, UserProfile
from src.core.calorie_calc import (
    bmr_mifflin_st_jeor,
    tdee_from_bmr,
    calorie_target_for_goal,
    macro_split_daily
)
from src.agents.diet_agent import generate_and_save_plan
from src.agents.workout_agent import generate_weekly_workout, save_weekly_workout


def summarize_profile(profile: UserProfile) -> Dict:
    """Compute and return core numbers given a UserProfile."""
    bmr = bmr_mifflin_st_jeor(profile.sex, profile.weight_kg, profile.height_cm, profile.age)
    tdee = tdee_from_bmr(bmr, profile.activity_level)
    target = calorie_target_for_goal(
        tdee,
        profile.goal,
        profile.target_rate_kg_per_week or 0.5
    )
    macros = macro_split_daily(target, profile.weight_kg)
    out = {
        "profile": asdict(profile),
        "bmr": bmr,
        "tdee": tdee,
        "calorie_target": target,
        "macros": macros
    }
    return out


def run_from_session():
    """
    Main coordinator function.
    - Requires that src.cli.onboard has been run at least once
      so that session_profile.json exists.
    """
    profile = load_profile()
    if not profile:
        raise RuntimeError("No session profile found. Run `python -m src.cli.onboard` first.")

    summary = summarize_profile(profile)

    # ----- Print summary -----
    print("=== DesiFit Summary ===")
    print(f"Name: {profile.name}")
    print(f"Age: {profile.age}")
    print(f"Goal: {profile.goal}")
    print(f"Dietary preferences: {profile.dietary_preferences}")
    print()
    print(f"BMR: {summary['bmr']} kcal/day")
    print(f"TDEE: {summary['tdee']} kcal/day")
    print(f"Daily calorie target: {summary['calorie_target']} kcal/day")
    print("Macros (daily):")
    for k, v in summary["macros"].items():
        print(f"  {k}: {v}")
    print()

    calorie_target = summary["calorie_target"]

    # ----- Diet Agent: weekly meal plan -----
    print("=== Generating Weekly Meal Plan (7 days) ===")
    meal_plan = generate_and_save_plan(
        user_profile=profile,
        calorie_target=calorie_target,
        filepath="meal_plan.json"
    )
    print("Saved meal_plan.json")
    print(f"Days in plan: {len(meal_plan['days'])}")
    print()

    # ----- Workout Agent: weekly workout plan -----
    print("=== Workout Plan (Week 1) ===")
    workout = generate_weekly_workout(
        goal=profile.goal,
        days_per_week=4,
        equipment="gym",  # future: make this user input
        week_index=0
    )
    save_weekly_workout(workout, "workout_plan.json")
    print("Saved workout_plan.json")
    print(f"Workouts per week: {workout['days_per_week']}")
    print()

    print("Done. You can now inspect meal_plan.json and workout_plan.json.")
    return {
        "summary": summary,
        "meal_plan": meal_plan,
        "workout_plan": workout,
    }
print("\n=== Grocery List (Week 1) ===")
grocery = generate_and_save_grocery_list("meal_plan.json")
print(grocery)



if __name__ == "__main__":
    run_from_session()
