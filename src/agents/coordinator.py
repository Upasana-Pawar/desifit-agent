# src/agents/coordinator.py
"""
Coordinator skeleton for DesiFit agent.
This module demonstrates the orchestration pattern:
- gather user profile
- call calorie calculator
- dispatch to diet/workout agents (not implemented today)
Keep this file lightweight for Day 1.
"""
from dataclasses import asdict
from src.core.user_profile import load_profile, UserProfile
from src.core.calorie_calc import (
    bmr_mifflin_st_jeor,
    tdee_from_bmr,
    calorie_target_for_goal,
    macro_split_daily
)

def summarize_profile(profile: UserProfile) -> dict:
    bmr = bmr_mifflin_st_jeor(profile.sex, profile.weight_kg, profile.height_cm, profile.age)
    tdee = tdee_from_bmr(bmr, profile.activity_level)
    target = calorie_target_for_goal(tdee, profile.goal, profile.target_rate_kg_per_week or 0.5)
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
    profile = load_profile()
    if not profile:
        raise RuntimeError("No session profile found. Run onboard CLI first.")
    summary = summarize_profile(profile)
    # For Day 1 we just print the summary; later this would be a message back to user
    print("=== DesiFit Summary ===")
    print(f"Name: {profile.name}")
    print(f"BMR: {summary['bmr']} kcal/day")
    print(f"TDEE: {summary['tdee']} kcal/day")
    print(f"Daily calorie target (goal={profile.goal}): {summary['calorie_target']} kcal/day")
    print("Macros (daily):")
    for k, v in summary['macros'].items():
        print(f"  {k}: {v}")
    return summary
