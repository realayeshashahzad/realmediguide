"""
MediGuide AI - Utility Functions

This file contains helper functions for:
- Safe JSON parsing
- Removing Markdown JSON fences
- Validating assessment output
- Input validation
- Cleaning model responses
"""


import json
import re


# ============================================================
# REQUIRED JSON FIELDS
# ============================================================

REQUIRED_FIELDS = [
    "summary",
    "possible_conditions",
    "urgency_level",
    "recommended_next_steps",
    "questions_for_doctor",
    "warning_signs",
]


# ============================================================
# VALID URGENCY LEVELS
# ============================================================

VALID_URGENCY_LEVELS = [
    "LOW",
    "MEDIUM",
    "HIGH",
    "EMERGENCY",
]


# ============================================================
# REMOVE JSON MARKDOWN FENCES
# ============================================================

def clean_json_text(raw_text):
    """
    Remove accidental Markdown code fences and surrounding
    text from the model response.

    Example:

        ```json
        {"summary": "..."}
        ```

    becomes:

        {"summary": "..."}
    """

    if raw_text is None:
        return ""

    text = str(raw_text).strip()

    # Remove ```json at the beginning
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Remove ``` at the end
    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    return text.strip()


# ============================================================
# EXTRACT JSON OBJECT
# ============================================================

def extract_json_object(text):
    """
    Try to extract the JSON object from surrounding text.

    This protects the application if the LLM returns something
    like:

        Here is the assessment:
        {"summary": "..."}
    """

    if not text:
        return ""

    text = text.strip()

    # First try to find the first { and last }
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:

        return text[start:end + 1]

    return text


# ============================================================
# SAFE JSON PARSER
# ============================================================

def safe_json_parse(raw_output):
    """
    Safely parse the LLM response as JSON.

    The application must never crash because of invalid JSON.

    Args:
        raw_output (str):
            Raw response returned by the LLM.

    Returns:
        dict:
            Parsed assessment or a safe fallback structure.
    """

    # --------------------------------------------------------
    # Clean response
    # --------------------------------------------------------

    cleaned_text = clean_json_text(
        raw_output
    )

    # --------------------------------------------------------
    # Extract JSON object
    # --------------------------------------------------------

    json_text = extract_json_object(
        cleaned_text
    )

    # --------------------------------------------------------
    # Try parsing
    # --------------------------------------------------------

    try:

        parsed = json.loads(
            json_text
        )

    except (json.JSONDecodeError, TypeError):

        return create_fallback_result(
            raw_output
        )

    # --------------------------------------------------------
    # Ensure dictionary
    # --------------------------------------------------------

    if not isinstance(parsed, dict):

        return create_fallback_result(
            raw_output
        )

    # --------------------------------------------------------
    # Normalize structure
    # --------------------------------------------------------

    return normalize_result(
        parsed
    )


# ============================================================
# NORMALIZE RESULT
# ============================================================

def normalize_result(result):
    """
    Ensure the assessment result contains all required fields.

    Missing fields receive safe default values.
    """

    normalized = {
        "summary": result.get(
            "summary",
            "No summary was generated.",
        ),

        "possible_conditions": result.get(
            "possible_conditions",
            [],
        ),

        "urgency_level": str(
            result.get(
                "urgency_level",
                "MEDIUM",
            )
        ).upper(),

        "recommended_next_steps": result.get(
            "recommended_next_steps",
            [],
        ),

        "questions_for_doctor": result.get(
            "questions_for_doctor",
            [],
        ),

        "warning_signs": result.get(
            "warning_signs",
            [],
        ),
    }

    # --------------------------------------------------------
    # Validate urgency
    # --------------------------------------------------------

    if normalized["urgency_level"] not in VALID_URGENCY_LEVELS:

        normalized["urgency_level"] = "MEDIUM"

    # --------------------------------------------------------
    # Ensure list fields are actually lists
    # --------------------------------------------------------

    list_fields = [
        "possible_conditions",
        "recommended_next_steps",
        "questions_for_doctor",
        "warning_signs",
    ]

    for field in list_fields:

        if not isinstance(
            normalized[field],
            list,
        ):

            normalized[field] = []

    return normalized


# ============================================================
# FALLBACK RESULT
# ============================================================

def create_fallback_result(raw_output=""):
    """
    Create a safe fallback response when JSON parsing fails.

    The application will not crash if the model returns invalid
    JSON.
    """

    return {
        "summary": (
            "The AI response could not be safely structured. "
            "Please consult a qualified healthcare professional "
            "for proper evaluation."
        ),

        "possible_conditions": [],

        "urgency_level": "MEDIUM",

        "recommended_next_steps": [
            "Consult a qualified healthcare professional.",
            "Do not use this AI response as a diagnosis.",
            "Seek urgent medical help if symptoms become severe."
        ],

        "questions_for_doctor": [
            "What could be causing these symptoms?",
            "Do I need an in-person medical evaluation?",
            "What warning signs should I watch for?"
        ],

        "warning_signs": [
            "Severe or rapidly worsening symptoms.",
            "Difficulty breathing.",
            "Severe chest pain.",
            "Loss of consciousness.",
            "Any situation that feels like a medical emergency."
        ],
    }


# ============================================================
# VALIDATE ASSESSMENT RESULT
# ============================================================

def validate_assessment_result(result):
    """
    Validate whether an assessment contains all required fields.

    Returns:
        bool: True if valid, otherwise False.
    """

    if not isinstance(
        result,
        dict,
    ):
        return False

    for field in REQUIRED_FIELDS:

        if field not in result:

            return False

    return True


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_inputs(age, symptoms):
    """
    Validate the minimum information required before calling
    the OpenAI API.

    The assignment requires:
    - Age
    - At least one symptom

    Returns:
        str or None:
            Error message if invalid, otherwise None.
    """

    # --------------------------------------------------------
    # Validate age
    # --------------------------------------------------------

    if not age or not str(age).strip():

        return "⚠️ Please enter the patient's age."

    # --------------------------------------------------------
    # Convert age to integer
    # --------------------------------------------------------

    try:

        age_number = int(
            str(age).strip()
        )

    except ValueError:

        return "⚠️ Age must be a valid number."

    # --------------------------------------------------------
    # Validate age range
    # --------------------------------------------------------

    if age_number <= 0:

        return "⚠️ Age must be greater than 0."

    if age_number > 120:

        return "⚠️ Please enter a realistic age."

    # --------------------------------------------------------
    # Validate symptoms
    # --------------------------------------------------------

    if not symptoms:

        return (
            "⚠️ Please select or enter at least one symptom "
            "before starting the assessment."
        )

    # --------------------------------------------------------
    # Validate empty symptom strings
    # --------------------------------------------------------

    valid_symptoms = [
        symptom
        for symptom in symptoms
        if str(symptom).strip()
    ]

    if not valid_symptoms:

        return (
            "⚠️ Please provide at least one symptom."
        )

    return None


# ============================================================
# FORMAT PATIENT DATA
# ============================================================

def format_patient_data(patient_data):
    """
    Convert patient data into a readable text format.

    Useful for debugging and displaying patient information.
    """

    if not isinstance(
        patient_data,
        dict,
    ):

        return ""

    lines = []

    for key, value in patient_data.items():

        lines.append(
            f"{key}: {value}"
        )

    return "\n".join(lines)


# ============================================================
# URGENCY COLOR HELPER
# ============================================================

def get_urgency_message(urgency):
    """
    Return a user-friendly message for each urgency level.
    """

    urgency = str(
        urgency
    ).upper()

    messages = {

        "LOW":
            "🟢 LOW — Continue monitoring and consider "
            "professional advice if symptoms persist or worsen.",

        "MEDIUM":
            "🟠 MEDIUM — Consider contacting a healthcare "
            "professional for evaluation.",

        "HIGH":
            "🔴 HIGH — Seek prompt professional medical "
            "evaluation.",

        "EMERGENCY":
            "🚨 EMERGENCY — Seek emergency medical help immediately.",
    }

    return messages.get(
        urgency,
        "⚠️ Please consult a qualified healthcare professional.",
    )


# ============================================================
# SAFETY CHECK
# ============================================================

def ensure_medical_safety(result):
    """
    Apply a final safety check to the generated result.

    This does not replace the system prompt. It is an additional
    application-level safety layer.
    """

    if not isinstance(
        result,
        dict,
    ):

        return create_fallback_result()

    result = normalize_result(
        result
    )

    # --------------------------------------------------------
    # Ensure possible conditions are educational
    # --------------------------------------------------------

    safe_conditions = []

    for condition in result["possible_conditions"]:

        if isinstance(
            condition,
            dict,
        ):

            name = condition.get(
                "name",
                "Possible condition",
            )

            reason = condition.get(
                "reason",
                "Educational information only.",
            )

            safe_conditions.append(
                {
                    "name": str(name),
                    "reason": str(reason),
                }
            )

    result["possible_conditions"] = safe_conditions

    # --------------------------------------------------------
    # Emergency safety reminder
    # --------------------------------------------------------

    if result["urgency_level"] == "EMERGENCY":

        emergency_message = (
            "Seek emergency medical help immediately."
        )

        if emergency_message not in result[
            "recommended_next_steps"
        ]:

            result["recommended_next_steps"].insert(
                0,
                emergency_message,
            )

    return result