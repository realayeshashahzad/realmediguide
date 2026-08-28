"""
MediGuide AI - Configuration File

This file contains:
- Application settings
- OpenAI model configuration
- Streamlit form options
- Medical safety settings

API keys are NOT stored in this file.
Users provide their own API key at runtime.
"""

# ============================================================
# APPLICATION INFORMATION
# ============================================================

APP_NAME = "MediGuide AI"

APP_DESCRIPTION = (
    "AI-Powered Medical Symptom Assessment and "
    "Patient Guidance Assistant"
)


# ============================================================
# OPENAI CONFIGURATION
# ============================================================

# Default OpenAI model
OPENAI_MODEL = "gpt-4o-mini"


# ============================================================
# FORM OPTIONS
# ============================================================

# Gender options for the patient form
GENDERS = [
    "Prefer not to say",
    "Female",
    "Male",
    "Other",
]


# Common symptoms
SYMPTOMS = [
    "Fever",
    "Cough",
    "Sore throat",
    "Runny nose",
    "Nasal congestion",
    "Headache",
    "Dizziness",
    "Fatigue",
    "Nausea",
    "Vomiting",
    "Diarrhea",
    "Abdominal pain",
    "Back pain",
    "Chest pain",
    "Shortness of breath",
    "Difficulty breathing",
    "Body aches",
    "Joint pain",
    "Muscle pain",
    "Rash",
    "Chills",
    "Loss of appetite",
    "Swelling",
    "Weakness",
]


# Duration options
DURATIONS = [
    "Less than 24 hours",
    "1-3 days",
    "4-7 days",
    "1-2 weeks",
    "More than 2 weeks",
    "More than 1 month",
    "Not sure",
]


# Supported answer languages
LANGUAGES = [
    "English",
    "Urdu",
]


# ============================================================
# URGENCY LEVELS
# ============================================================

URGENCY_LEVELS = [
    "LOW",
    "MEDIUM",
    "HIGH",
    "EMERGENCY",
]


# ============================================================
# CACHE CONFIGURATION
# ============================================================

# SQLite cache is no longer used in the public version.
# The application uses InMemoryCache only when caching
# is enabled by the user.

SQLITE_CACHE_PATH = "mediguide_cache.db"


# ============================================================
# SAFETY DISCLAIMER
# ============================================================

MEDICAL_DISCLAIMER = """
MediGuide AI is an educational AI prototype only.

It is NOT a doctor, medical device, emergency service,
professional diagnosis, or replacement for qualified
healthcare advice.

The application must never be used to make a confirmed
medical diagnosis or treatment decision.

If symptoms are severe, suddenly worsen, or appear
life-threatening, seek emergency medical help immediately.

Always consult a qualified healthcare professional.
"""


# ============================================================
# MODEL SETTINGS
# ============================================================

# Temperature is kept low because medical guidance should
# be consistent and avoid unnecessary creativity.

MODEL_TEMPERATURE = 0.0


# Maximum number of tokens requested from the model
MAX_OUTPUT_TOKENS = 1200