import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = "models/gemini-2.5-flash"
    
    # Safety settings
    BLOCKED_KEYWORDS = [
        "system prompt", "api key", "reveal", "ignore instructions",
        "bypass", "jailbreak", "pretend", "roleplay as"
    ]
    
    # Price ranges
    BUDGET_RANGES = {
        "under 15k": (0, 15000),
        "under 20k": (0, 20000),
        "under 25k": (0, 25000),
        "under 30k": (0, 30000),
        "under 40k": (0, 40000),
        "under 50k": (0, 50000),
        "flagship": (50000, 200000)
    }