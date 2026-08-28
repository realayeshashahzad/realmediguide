"""
MediGuide AI - Prompt Templates

This file contains all prompts used by the application.

LangChain concepts demonstrated:
1. PromptTemplate
2. ChatPromptTemplate
3. System + Human messages
4. Structured JSON output instructions
5. Medical safety instructions
"""

from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
)


# ============================================================
# JSON OUTPUT SCHEMA
# ============================================================

# IMPORTANT:
# Double curly braces {{ }} are used because LangChain
# treats single curly braces as template variables.

JSON_SCHEMA = """
{{
  "summary": "",
  "possible_conditions": [
    {{
      "name": "",
      "reason": ""
    }}
  ],
  "urgency_level": "",
  "recommended_next_steps": [],
  "questions_for_doctor": [],
  "warning_signs": []
}}
"""


# ============================================================
# SYSTEM SAFETY PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are MediGuide AI, an educational medical information
assistant.

Your purpose is to provide general educational guidance
based on symptoms and patient information.

IMPORTANT MEDICAL SAFETY RULES:

1. You are NOT a doctor.
2. You must NEVER claim to provide a confirmed diagnosis.
3. You must NEVER tell the user that they definitely have
   a particular disease or medical condition.
4. Possible conditions are for educational information only.
5. Encourage the user to consult a qualified healthcare
   professional.
6. If symptoms suggest a potentially serious or emergency
   situation, clearly recommend seeking urgent medical help.
7. For EMERGENCY urgency, explicitly tell the user to seek
   emergency medical help immediately.
8. Do not recommend prescription medication or specific
   medication doses.
9. Do not tell the user to stop or change prescribed
   medication.
10. Do not create false certainty.
11. Use calm, clear and understandable language.
12. Do not unnecessarily frighten the user.
13. If information is insufficient, clearly state that a
    healthcare professional should evaluate the situation.
14. Never replace professional medical assessment.

URGENCY LEVELS:

LOW:
Symptoms appear less concerning based on the provided
information. Recommend monitoring and routine professional
advice if symptoms persist or worsen.

MEDIUM:
Symptoms may require professional evaluation, especially
if they continue or worsen.

HIGH:
Symptoms may require prompt medical evaluation.

EMERGENCY:
Potentially serious symptoms are present. Tell the user to
seek emergency medical help immediately.

IMPORTANT:

Return ONLY valid JSON.

Do not use Markdown.

Do not add json code fences.

Do not add explanations before or after the JSON.

The possible conditions are educational possibilities only.
They must never be presented as confirmed diagnoses.

The urgency_level MUST be exactly one of:

LOW
MEDIUM
HIGH
EMERGENCY
"""


# ============================================================
# HUMAN PROMPT
# ============================================================

HUMAN_PROMPT = """
Assess the following patient information for educational
medical guidance.

PATIENT INFORMATION

Age:
{age}

Gender:
{gender}

Symptoms:
{symptoms}

Duration:
{duration}

Severity:
{severity}/10

Existing medical conditions:
{existing_conditions}

Current medications:
{medications}

Additional notes:
{additional_notes}

Answer language:
{language}

TASK

Provide a safety-focused educational assessment.

The response MUST:

- Summarize the symptoms.
- List possible conditions only for educational purposes.
- Explain why each possible condition may be relevant.
- Assign an urgency level.
- Provide appropriate next steps.
- Provide questions the patient can ask a healthcare
  professional.
- Provide warning signs that require immediate attention.
- Avoid confirmed diagnoses.
- Avoid medication prescriptions.
- Encourage professional medical evaluation.

Return ONLY the required JSON object.

The required JSON structure is:

{{
  "summary": "",
  "possible_conditions": [
    {{
      "name": "",
      "reason": ""
    }}
  ],
  "urgency_level": "",
  "recommended_next_steps": [],
  "questions_for_doctor": [],
  "warning_signs": []
}}
"""


# ============================================================
# PROMPT TEMPLATE
# ============================================================

# This demonstrates LangChain's PromptTemplate.
# It creates a reusable single-string prompt.

PATIENT_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=[
        "age",
        "gender",
        "symptoms",
        "duration",
        "severity",
        "existing_conditions",
        "medications",
        "additional_notes",
        "language",
    ],
    template=HUMAN_PROMPT,
)


# ============================================================
# CHAT PROMPT TEMPLATE
# ============================================================

# This demonstrates LangChain's ChatPromptTemplate.
#
# The system message defines the AI's role and safety rules.
# The human message contains the patient's information.

ASSESSMENT_CHAT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_PROMPT,
        ),
        (
            "human",
            HUMAN_PROMPT,
        ),
    ]
)


# ============================================================
# STREAMING NARRATIVE SYSTEM PROMPT
# ============================================================

NARRATIVE_SYSTEM_PROMPT = """
You are MediGuide AI.

Generate a short, clear and supportive educational
medical guidance narrative based on the patient's
information.

IMPORTANT:

- You are not a doctor.
- Do not provide a confirmed diagnosis.
- Do not claim certainty.
- Do not prescribe medication.
- Do not recommend medication doses.
- Do not tell the patient to stop or change medication.
- Encourage consultation with a qualified healthcare
  professional.
- If the situation appears urgent or dangerous, clearly
  advise seeking immediate medical help.
- Keep the language understandable.
- Respond in the requested language.

This narrative is educational information only and is not
a substitute for professional medical care.
"""


# ============================================================
# STREAMING NARRATIVE HUMAN PROMPT
# ============================================================

NARRATIVE_HUMAN_PROMPT = """
Patient information:

Age: {age}
Gender: {gender}
Symptoms: {symptoms}
Duration: {duration}
Severity: {severity}/10
Existing conditions: {existing_conditions}
Current medications: {medications}
Additional notes: {additional_notes}
Requested language: {language}

Write a concise educational guidance narrative.

Include:

1. What the symptoms may generally indicate.
2. What the patient should consider doing next.
3. When professional medical evaluation is appropriate.
4. Warning signs that require urgent medical attention.

Do NOT provide a confirmed diagnosis.

Do NOT prescribe medication.

Do NOT recommend medication doses.

Do NOT tell the patient to stop or change prescribed
medication.

Use the requested language.

Remember:
This is educational information only and is not a
replacement for a qualified healthcare professional.
"""


# ============================================================
# STREAMING CHAT TEMPLATE
# ============================================================

NARRATIVE_CHAT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            NARRATIVE_SYSTEM_PROMPT,
        ),
        (
            "human",
            NARRATIVE_HUMAN_PROMPT,
        ),
    ]
)


# ============================================================
# MESSAGE DEMO PROMPT
# ============================================================

MESSAGE_DEMO_SYSTEM = """
You are MediGuide AI.

You provide educational medical information only.

Never provide a confirmed diagnosis.

Always encourage consultation with a qualified
healthcare professional.

If symptoms appear urgent, recommend seeking
appropriate urgent medical help.
"""


MESSAGE_DEMO_HUMAN = """
The patient has provided symptoms and wants general
educational information.

Explain how an AI assistant should safely respond
without claiming a diagnosis.
"""


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_assessment_messages(patient_data):
    """
    Create chat messages for the patient's assessment.

    Args:
        patient_data (dict):
            Dictionary containing patient information.

    Returns:
        list:
            LangChain chat messages.
    """

    return ASSESSMENT_CHAT_TEMPLATE.format_messages(
        **patient_data
    )


# ============================================================
# NARRATIVE MESSAGE HELPER
# ============================================================

def get_narrative_messages(patient_data):
    """
    Create chat messages for streaming guidance.

    Args:
        patient_data (dict):
            Dictionary containing patient information.

    Returns:
        list:
            LangChain chat messages.
    """

    return NARRATIVE_CHAT_TEMPLATE.format_messages(
        **patient_data
    )


# ============================================================
# GET JSON SCHEMA
# ============================================================

def get_json_schema():
    """
    Return the required JSON schema.

    The double curly braces are converted into normal
    curly braces for display/use outside a template.
    """

    return JSON_SCHEMA.replace(
        "{{",
        "{"
    ).replace(
        "}}",
        "}"
    )