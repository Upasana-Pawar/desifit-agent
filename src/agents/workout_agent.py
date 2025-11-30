# src/agents/workout_agent.py
"""
Workout agent for DesiFit.

Goal:
- Generate a simple, structured weekly workout plan based on:
    - goal: 'lose_weight' | 'maintain' | 'gain_weight'
    - days_per_week: e.g., 3 or 4
    - equipment: 'gym' or 'home'
    - week_index: which week (0-based) for progression

This is intentionally simple but structured and easy to extend later.
"""

from typing import Dict, List


def _base_exercises_gym() -> Dict[str, List[str]]:
    """Return a dictionary of basic gym exercises grouped by muscle."""
    return {
        "full_body": [
            "Squats (barbell or smith machine)",
            "Romanian deadlifts",
            "Lat pulldown or assisted pull-ups",
            "Dumbbell bench press",
            "Seated cable row",
            "Plank"
        ],
        "upper_body": [
            "Incline dumbbell press",
            "Seated row",
            "Shoulder press",
            "Lat pulldown",
            "Dumbbell bicep curls",
            "Tricep pushdowns"
        ],
        "lower_body": [
            "Leg press",
            "Lunges",
            "Hamstring curls",
            "Calf raises",
            "Glute bridges"
        ],
        "cardio": [
            "Treadmill walk (incline)",
            "Cycling",
            "Elliptical"
        ]
    }


def _base_exercises_home() -> Dict[str, List[str]]:
    """Return a dictionary of basic home exercises grouped by pattern."""
    return {
        "full_body": [
            "Bodyweight squats",
            "Glute bridges",
            "Incline push-ups",
            "Bent-over backpack rows",
            "Dead bugs",
            "Plank"
        ],
        "upper_body": [
            "Knee push-ups",
            "Chair dips",
            "Backpack rows",
            "Wall slides"
        ],
        "lower_body": [
            "Reverse lunges",
            "Glute bridges",
            "Calf raises on a step",
            "Wall sit"
        ],
        "cardio": [
            "Brisk walk",
            "March in place",
            "Skipping (if joints allow)"
        ]
    }


def _suggest_sets_reps(goal: str) -> Dict[str, str]:
    """
    Suggest sets/reps based on goal.
    - lose_weight: slightly higher reps, moderate sets.
    - gain_weight: moderate reps, slightly heavier sets.
    - maintain: middle ground.
    """
    goal = goal or "lose_weight"
    if goal == "gain_weight":
        return {"strength": "3–4 sets x 6–10 reps", "accessory": "2–3 sets x 10–12 reps", "cardio": "10–15 min"}
    elif goal == "maintain":
        return {"strength": "3 sets x 8–12 reps", "accessory": "2–3 sets x 10–15 reps", "cardio": "10–20 min"}
    else:  # lose_weight
        return {"strength": "3 sets x 10–15 reps", "accessory": "2–3 sets x 12–15 reps", "cardio": "20–30 min"}


def generate_workout_day(
    goal: str,
    equipment: str,
    day_index: int
) -> Dict:
    """
    Generate a single day's workout.
    - Uses a simple 4-day split pattern if possible.
    """
    equipment = (equipment or "gym").lower()
    base = _base_exercises_gym() if equipment == "gym" else _base_exercises_home()
    scheme = _suggest_sets_reps(goal)

    # Map day index to focus area. This is a simple pattern:
    # Day 0: Full body + light cardio
    # Day 1: Upper + core
    # Day 2: Lower + cardio
    # Day 3: Full body + cardio (lighter)
    focus_patterns = ["full_body", "upper_body", "lower_body", "full_body"]
    focus = focus_patterns[day_index % len(focus_patterns)]

    exercises = []

    if focus == "full_body":
        for ex in base["full_body"][:4]:
            exercises.append({"name": ex, "scheme": scheme["strength"]})
        exercises.append({"name": base["cardio"][0], "scheme": scheme["cardio"]})
    elif focus == "upper_body":
        for ex in base["upper_body"]:
            exercises.append({"name": ex, "scheme": scheme["strength"]})
        exercises.append({"name": "Plank or dead bugs", "scheme": scheme["accessory"]})
    elif focus == "lower_body":
        for ex in base["lower_body"]:
            exercises.append({"name": ex, "scheme": scheme["strength"]})
        exercises.append({"name": base["cardio"][1], "scheme": scheme["cardio"]})

    return {
        "day_index": day_index,
        "focus": focus,
        "equipment": equipment,
        "goal": goal,
        "exercises": exercises
    }


def generate_weekly_workout(
    goal: str,
    days_per_week: int = 3,
    equipment: str = "gym",
    week_index: int = 0
) -> Dict:
    """
    Generate a weekly workout plan (dictionary).
    - days_per_week: how many sessions per week (e.g. 3 or 4).
    - week_index: used for future progression logic (currently just echoed).
    """
    days = []
    for i in range(days_per_week):
        day_plan = generate_workout_day(goal=goal, equipment=equipment, day_index=i)
        days.append(day_plan)

    plan = {
        "week_index": week_index,
        "goal": goal,
        "days_per_week": days_per_week,
        "equipment": equipment,
        "days": days
    }
    return plan


def save_weekly_workout(plan: Dict, filepath: str = "workout_plan.json") -> str:
    """Save weekly workout plan to JSON file."""
    import json
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)
    return filepath


if __name__ == "__main__":
    # Quick manual test
    demo = generate_weekly_workout(goal="lose_weight", days_per_week=4, equipment="gym", week_index=0)
    save_weekly_workout(demo)
    print("Saved workout_plan.json")
