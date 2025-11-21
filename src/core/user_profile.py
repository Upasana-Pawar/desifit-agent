# src/core/user_profile.py
import json
from dataclasses import dataclass, asdict
from typing import Optional

SESSION_FILE = "session_profile.json"

@dataclass
class UserProfile:
    name: str
    age: int           # years
    sex: str           # 'male' or 'female'
    height_cm: float
    weight_kg: float
    activity_level: str  # one of: 'sedentary','light','moderate','active','very_active'
    goal: str          # 'lose_weight'|'maintain'|'gain_weight'
    target_rate_kg_per_week: Optional[float] = None  # e.g., 0.5 kg/week
    dietary_preferences: Optional[str] = None  # e.g., 'vegetarian', 'no onion', 'vegan'

def save_profile(profile: UserProfile, filepath: str = SESSION_FILE):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(asdict(profile), f, indent=2)

def load_profile(filepath: str = SESSION_FILE) -> Optional[UserProfile]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return UserProfile(**data)
    except FileNotFoundError:
        return None
