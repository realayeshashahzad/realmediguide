import sys
import os
#Root folder path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st

from src.config import (
    APP_NAME,
    APP_DESCRIPTION,
    GENDERS,
    SYMPTOMS,
    DURATIONS,
    LANGUAGES,
)

from src.chains import assess_patient, stream_narrative
from src.cache_manager import set_cache
from src.utils import validate_inputs


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MediGuide AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 20px;
    }

    .medical-disclaimer {
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #ff9800;
        background-color: #fff8e1;
        color: #333333;
        margin-bottom: 20px;
    }

    .medical-disclaimer strong {
        color: #d84315;
    }

    .emergency-box {
        padding: 18px;
        border-radius: 10px;
        border: 2px solid #d32f2f;
        background-color: #ffebee;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🩺 MediGuide AI")

    st.write(APP_DESCRIPTION)

    st.divider()

    # --------------------------------------------------------
    # API KEY
    # --------------------------------------------------------

    st.subheader("🔑 OpenAI API Key")

    user_api_key = st.text_input(
        "Enter your own OpenAI API key",
        type="password",
        placeholder="sk-...",
        help=(
            "Your API key is used for this session only. "
            "Do not share your API key with anyone."
        ),
    )

    if user_api_key:
        st.success("API key entered ✓")
    else:
        st.info(
            "Please enter your OpenAI API key "
            "before using the AI assessment."
        )

    st.divider()

    # --------------------------------------------------------
    # MEDICAL SAFETY
    # --------------------------------------------------------

    st.subheader("⚠️ Medical Safety Notice")

    st.warning(
        """
        MediGuide AI is an educational AI prototype only.

        It is NOT a doctor, medical device, professional diagnosis,
        emergency service, or replacement for qualified healthcare advice.

        Never use this application to make a medical diagnosis or
        treatment decision.

        If symptoms are severe or life-threatening, seek emergency
        medical help immediately.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # MODEL CONFIGURATION
    # --------------------------------------------------------

    st.subheader("⚙️ Model Configuration")

    model_name = st.text_input(
        "Model",
        value="gpt-4o-mini",
        disabled=True,
    )

    st.caption(f"Selected model: {model_name}")

    st.divider()

    # --------------------------------------------------------
    # LANGUAGE
    # --------------------------------------------------------

    st.subheader("🌐 Language")

    sidebar_language = st.selectbox(
        "Default answer language",
        LANGUAGES,
        index=0,
    )

    st.divider()

    # --------------------------------------------------------
    # CACHE
    # --------------------------------------------------------

    st.subheader("💾 Cache")

    # Public version:
    # Use only InMemoryCache.
    cache_enabled = st.checkbox(
        "Enable in-memory caching",
        value=False,
        help=(
            "Caching is disabled by default for privacy. "
            "If enabled, responses remain only in application memory "
            "and are lost when the app restarts."
        ),
    )

    cache_type = "InMemoryCache"

    if cache_enabled:
        set_cache(cache_type)

    st.divider()

    st.caption(
        "For educational purposes only. Always consult a qualified "
        "healthcare professional."
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🩺 MediGuide AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Medical Symptom Assessment and Patient Guidance Assistant'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# MAIN DISCLAIMER
# ============================================================

# ============================================================
# MAIN DISCLAIMER
# ============================================================

st.markdown(
    '<div class="medical-disclaimer">'
    '<strong>⚠️ Important Medical Disclaimer</strong><br><br>'
    'This application provides general educational information only. '
    'It does not provide a confirmed diagnosis and is not a replacement '
    'for a licensed doctor, professional medical advice, treatment, '
    'or emergency services.'
    '<br><br>'
    '<strong>'
    'If you believe you are experiencing a medical emergency, '
    'seek emergency medical help immediately.'
    '</strong>'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# PATIENT INFORMATION FORM
# ============================================================

st.header("👤 Patient Information")

col1, col2 = st.columns(2)

with col1:

    age = st.text_input(
        "Patient Age *",
        placeholder="e.g. 25",
        help="Enter the patient's age.",
    )

with col2:

    gender = st.selectbox(
        "Gender *",
        GENDERS,
    )


# ============================================================
# SYMPTOMS
# ============================================================

st.header("🩹 Symptoms")

symptoms = st.multiselect(
    "Select symptoms *",
    SYMPTOMS,
    help="Select all symptoms that apply.",
)

additional_symptoms = st.text_area(
    "Other symptoms",
    placeholder="Describe any additional symptoms...",
    height=100,
)


# ============================================================
# DURATION AND SEVERITY
# ============================================================

col1, col2 = st.columns(2)

with col1:

    duration = st.selectbox(
        "Duration of symptoms *",
        DURATIONS,
    )

with col2:

    severity = st.slider(
        "Overall symptom severity (1–10)",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
    )


# ============================================================
# MEDICAL CONTEXT
# ============================================================

st.header("📋 Medical Context")

existing_conditions = st.text_area(
    "Existing medical conditions",
    placeholder=(
        "Example: diabetes, hypertension, asthma, "
        "or write 'None' if applicable."
    ),
    height=100,
)

medications = st.text_area(
    "Current medications",
    placeholder=(
        "List current medications if known, "
        "or write 'None'."
    ),
    height=100,
)

additional_notes = st.text_area(
    "Additional notes",
    placeholder=(
        "Anything else the healthcare professional "
        "should know..."
    ),
    height=100,
)


# ============================================================
# LANGUAGE
# ============================================================

answer_language = st.selectbox(
    "Answer language",
    LANGUAGES,
    index=(
        LANGUAGES.index(sidebar_language)
        if sidebar_language in LANGUAGES
        else 0
    ),
)


# ============================================================
# SUBMIT BUTTON
# ============================================================

st.divider()

submit = st.button(
    "🔍 Assess Symptoms",
    type="primary",
    use_container_width=True,
)


# ============================================================
# PROCESS REQUEST
# ============================================================

if submit:

    # --------------------------------------------------------
    # Check API Key
    # --------------------------------------------------------

    if not user_api_key or not user_api_key.strip():

        st.error(
            "🔑 Please enter your OpenAI API key in the sidebar "
            "before using the AI assessment."
        )

        st.stop()

    # --------------------------------------------------------
    # Clean API key
    # --------------------------------------------------------

    user_api_key = user_api_key.strip()

    # --------------------------------------------------------
    # Combine selected and free-text symptoms
    # --------------------------------------------------------

    all_symptoms = list(symptoms)

    if additional_symptoms.strip():

        all_symptoms.append(
            additional_symptoms.strip()
        )

    # --------------------------------------------------------
    # Validate user input
    # --------------------------------------------------------

    validation_error = validate_inputs(
        age=age,
        symptoms=all_symptoms,
    )

    if validation_error:

        st.error(validation_error)

        st.stop()

    # --------------------------------------------------------
    # Prepare patient information
    # --------------------------------------------------------

    patient_data = {
        "age": age,
        "gender": gender,
        "symptoms": ", ".join(all_symptoms),
        "duration": duration,
        "severity": severity,
        "existing_conditions": existing_conditions,
        "medications": medications,
        "additional_notes": additional_notes,
        "language": answer_language,
    }

    # --------------------------------------------------------
    # Safety warning
    # --------------------------------------------------------

    st.info(
        "The information below is educational guidance only. "
        "Please consult a qualified healthcare professional "
        "for proper evaluation."
    )

    # --------------------------------------------------------
    # Generate assessment
    # --------------------------------------------------------

    with st.spinner("Analyzing the provided information..."):

        try:

            result = assess_patient(
                patient_data,
                api_key=user_api_key,
                cache_enabled=cache_enabled,
                cache_type=cache_type,
            )

        except Exception as error:

            st.error(
                "Sorry, the assessment could not be generated. "
                "Please check your API key and try again."
            )

            st.expander(
                "Technical details"
            ).write(str(error))

            st.stop()

    # ========================================================
    # RESULTS DASHBOARD
    # ========================================================

    st.divider()

    st.header("📊 Assessment Dashboard")

    # --------------------------------------------------------
    # Urgency
    # --------------------------------------------------------

    urgency = result.get(
        "urgency_level",
        "UNKNOWN",
    ).upper()

    if urgency == "EMERGENCY":

        st.error(
            "🚨 EMERGENCY LEVEL — "
            "Seek emergency medical help immediately."
        )

    elif urgency == "HIGH":

        st.error(
            "🔴 HIGH URGENCY — "
            "Please seek prompt professional medical advice."
        )

    elif urgency == "MEDIUM":

        st.warning(
            "🟠 MEDIUM URGENCY — "
            "Consider contacting a healthcare professional."
        )

    elif urgency == "LOW":

        st.success(
            "🟢 LOW URGENCY — "
            "Continue monitoring symptoms and consider "
            "professional advice if symptoms persist or worsen."
        )

    else:

        st.warning(
            f"Urgency level: {urgency}"
        )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:

        st.metric(
            "Urgency Level",
            urgency,
        )

    with metric_col2:

        st.metric(
            "Symptom Severity",
            f"{severity}/10",
        )

    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📝 Summary",
            "🧠 General Information",
            "👨‍⚕️ Next Steps",
            "⚠️ Warning Signs",
        ]
    )

    # --------------------------------------------------------
    # TAB 1 — SUMMARY
    # --------------------------------------------------------

    with tab1:

        st.subheader("Patient Symptom Summary")

        st.write(
            result.get(
                "summary",
                "No summary was generated.",
            )
        )

        st.divider()

        st.subheader("Patient Information")

        info_col1, info_col2, info_col3 = st.columns(3)

        with info_col1:

            st.write(
                f"**Age:** {age}"
            )

        with info_col2:

            st.write(
                f"**Gender:** {gender}"
            )

        with info_col3:

            st.write(
                f"**Severity:** {severity}/10"
            )

        st.write(
            f"**Duration:** {duration}"
        )

        st.write(
            f"**Symptoms:** {', '.join(all_symptoms)}"
        )

    # --------------------------------------------------------
    # TAB 2 — GENERAL INFORMATION
    # --------------------------------------------------------

    with tab2:

        st.subheader("Possible Conditions")

        st.info(
            "These are possible conditions for educational "
            "information only. They are NOT confirmed diagnoses."
        )

        possible_conditions = result.get(
            "possible_conditions",
            [],
        )

        if possible_conditions:

            for condition in possible_conditions:

                if isinstance(condition, dict):

                    name = condition.get(
                        "name",
                        "Unknown",
                    )

                    reason = condition.get(
                        "reason",
                        "No explanation provided.",
                    )

                    with st.expander(name):

                        st.write(reason)

                else:

                    st.write(
                        f"- {condition}"
                    )

        else:

            st.write(
                "No possible conditions were returned."
            )

    # --------------------------------------------------------
    # TAB 3 — NEXT STEPS
    # --------------------------------------------------------

    with tab3:

        st.subheader("Recommended Next Steps")

        next_steps = result.get(
            "recommended_next_steps",
            [],
        )

        if next_steps:

            for step in next_steps:

                st.write(
                    f"• {step}"
                )

        else:

            st.write(
                "No next steps were provided."
            )

        st.divider()

        st.subheader(
            "Questions to Ask a Healthcare Professional"
        )

        questions = result.get(
            "questions_for_doctor",
            [],
        )

        if questions:

            for question in questions:

                st.write(
                    f"• {question}"
                )

        else:

            st.write(
                "No questions were generated."
            )

    # --------------------------------------------------------
    # TAB 4 — WARNING SIGNS
    # --------------------------------------------------------

    with tab4:

        st.subheader("⚠️ Warning Signs")

        warning_signs = result.get(
            "warning_signs",
            [],
        )

        if warning_signs:

            for warning in warning_signs:

                st.error(
                    f"⚠️ {warning}"
                )

        else:

            st.write(
                "No specific warning signs were returned."
            )

        st.divider()

        st.warning(
            "If symptoms become severe, suddenly worsen, or "
            "you believe you are experiencing an emergency, "
            "seek emergency medical help immediately."
        )

    # ========================================================
    # STREAMING NARRATIVE
    # ========================================================

    st.divider()

    st.header("💬 AI Guidance")

    st.info(
        "The following is general educational information, "
        "not a medical diagnosis."
    )

    try:

        stream_container = st.empty()

        with st.spinner("Generating guidance..."):

            streamed_text = st.write_stream(
                stream_narrative(
                    patient_data,
                    api_key=user_api_key,
                )
            )

    except Exception as error:

        st.warning(
            "The live guidance could not be streamed. "
            "The structured assessment above is still available."
        )

        st.expander(
            "Technical details"
        ).write(
            str(error)
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    """
    🩺 MediGuide AI — Educational AI Prototype

    This application is not a medical device and does not provide
    confirmed diagnoses or medical treatment.

    Always consult a qualified healthcare professional.
    For urgent or life-threatening situations, seek emergency help immediately.
    """
)