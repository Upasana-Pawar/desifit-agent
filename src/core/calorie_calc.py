# src/core/calorie_calc.py
from typing import Dict

def bmr_mifflin_st_jeor(sex: str, weight_kg: float, height_cm: float, age: int) -> float:
    """
    Mifflin-St Jeor BMR formula.
    For men: BMR = 10*weight + 6.25*height - 5*age + 5
    For women: BMR = 10*weight + 6.25*height - 5*age - 161
    """
    if sex.lower() in ("m", "male"):
        offset = 5
    else:
        offset = -161
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + offset
    return round(bmr, 2)

ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,        # little or no exercise
    "light": 1.375,          # light exercise 1-3 days/week
    "moderate": 1.55,        # moderate exercise 3-5 days/week
    "active": 1.725,         # hard exercise 6-7 days/week
    "very_active": 1.9       # very hard training or physical job
}

def tdee_from_bmr(bmr: float, activity_level: str) -> float:
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.375)
    return round(bmr * multiplier, 2)

def calorie_target_for_goal(tdee: float, goal: str, weekly_rate_kg: float = 0.5) -> float:
    """
    Estimate daily calorie target.
    - For weight loss: create a deficit; 0.5 kg/week ~= 3500 kcal/week -> 500 kcal/day
    - For weight gain: surplus (mirror)
    weekly_rate_kg default 0.5
    """
    kcal_per_kg = 7700  # conservative approx (7,700 kcal per kg)
    daily_delta = (weekly_rate_kg * kcal_per_kg) / 7.0
    if goal == "lose_weight":
        return round(tdee - daily_delta, 0)
    elif goal == "gain_weight":
        return round(tdee + daily_delta, 0)
    else:
        return round(tdee, 0)

def macro_split_daily(calorie_target: float, weight_kg: float,
                      protein_g_per_kg: float = 1.8,
                      fat_pct: float = 0.25) -> Dict[str, float]:
    """
    Compute daily macros:
      - Protein set by grams/kg (common range 1.6-2.2 g/kg; default 1.8)
      - Fat as percentage of calories (default 25%)
      - Carbs = remaining calories
    Returns grams of protein, fat, carbs and calories breakdown.
    """
    protein_g = round(weight_kg * protein_g_per_kg, 1)
    protein_cal = protein_g * 4

    fat_cal = calorie_target * fat_pct
    fat_g = round(fat_cal / 9, 1)

    remaining_cal = calorie_target - (protein_cal + fat_cal)
    carbs_g = round(remaining_cal / 4, 1) if remaining_cal > 0 else 0.0

    return {
        "calorie_target": round(calorie_target, 1),
        "protein_g": protein_g,
        "fat_g": fat_g,
        "carbs_g": carbs_g,
        "protein_cal": protein_cal,
        "fat_cal": round(fat_cal, 1),
        "carbs_cal": round(carbs_g * 4, 1)
    }
