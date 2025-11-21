# src/cli/onboard.py
import json
from src.core.user_profile import UserProfile, save_profile

def prompt(question, cast=str, default=None):
    raw = input(f"{question}{' ['+str(default)+']' if default is not None else ''}: ")
    if raw.strip() == "" and default is not None:
        return default
    return cast(raw)

def run_onboarding():
    print("Welcome to DesiFit onboarding (Day 1 CLI). Please enter basic info.")
    name = prompt("Name", str, "Upasana")
    age = prompt("Age (years)", int, 25)
    sex = prompt("Sex (male/female)", str, "female")
    height_cm = prompt("Height (cm)", float, 162.0)
    weight_kg = prompt("Weight (kg)", float, 70.0)
    print("Activity levels: sedentary, light, moderate, active, very_active")
    activity_level = prompt("Activity level", str, "light")
    print("Goals: lose_weight, maintain, gain_weight")
    goal = prompt("Goal", str, "lose_weight")
    target_rate = prompt("Target kg per week (e.g., 0.5)", float, 0.5)
    pref = prompt("Dietary preferences (e.g., vegetarian, no onion)", str, "vegetarian")

    profile = UserProfile(
        name=name,
        age=age,
        sex=sex,
        height_cm=height_cm,
        weight_kg=weight_kg,
        activity_level=activity_level,
        goal=goal,
        target_rate_kg_per_week=target_rate,
        dietary_preferences=pref
    )
    save_profile(profile)
    print("Profile saved to session_profile.json")

if __name__ == "__main__":
    run_onboarding()
