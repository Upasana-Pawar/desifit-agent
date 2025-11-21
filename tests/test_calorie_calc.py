# tests/test_calorie_calc.py
import pytest
from src.core.calorie_calc import (
    bmr_mifflin_st_jeor, tdee_from_bmr, calorie_target_for_goal, macro_split_daily
)

def test_bmr_male():
    bmr = bmr_mifflin_st_jeor("male", 70, 175, 30)
    # compute expected by formula: 10*70 + 6.25*175 -5*30 +5 = 700 + 1093.75 -150 +5 = 1648.75
    assert round(bmr, 2) == 1648.75

def test_bmr_female():
    bmr = bmr_mifflin_st_jeor("female", 60, 160, 25)
    # expected: 10*60 + 6.25*160 -5*25 -161 = 600 + 1000 -125 -161 = 1314
    assert round(bmr, 2) == 1314.0

def test_tdee_and_target():
    bmr = 1600
    tdee = tdee_from_bmr(bmr, "moderate")
    assert round(tdee, 2) == round(1600 * 1.55, 2)
    target = calorie_target_for_goal(tdee, "lose_weight", weekly_rate_kg=0.5)
    # daily delta = 0.5 * 7700 / 7 = 550
    assert target == round(tdee - 550, 0)

def test_macro_split():
    macros = macro_split_daily(1800, 70, protein_g_per_kg=1.8, fat_pct=0.25)
    assert macros["protein_g"] == 126.0  # 70 * 1.8
    assert macros["fat_g"] == round((1800 * 0.25) / 9, 1)
    assert macros["carbs_g"] >= 0
