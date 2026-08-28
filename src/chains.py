"""
MediGuide AI - LangChain Chains

This file contains:
- ChatOpenAI model
- LLMChain
- Patient assessment
- Streaming narrative
- System/Human/AI message demonstration

API KEY HANDLING:
- The API key is provided by the user at runtime.
- No personal API key is stored in this file.
- No API key is loaded from .env.
"""
from langchain_openai import ChatOpenAI
from langchain_classic.chains import LLMChain
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)

from src.config import (
    OPENAI_MODEL,
    MODEL_TEMPERATURE,
    MAX_OUTPUT_TOKENS,
)

from src.prompts import (
    SYSTEM_PROMPT,
    ASSESSMENT_CHAT_TEMPLATE,
    NARRATIVE_CHAT_TEMPLATE,
)

from src.utils import safe_json_parse


# ============================================================
# CREATE CHATOPENAI MODEL
# ============================================================

def create_llm(api_key):
    """
    Create and return the OpenAI chat model.

    The API key is supplied by the user at runtime.

    Args:
        api_key (str):
            User-provided OpenAI API key.

    Returns:
        ChatOpenAI:
            Configured OpenAI chat model.
    """

    if not api_key:
        raise ValueError(
            "OpenAI API key is required. "
            "Please enter your API key in the sidebar."
        )

    api_key = api_key.strip()

    if not api_key:
        raise ValueError(
            "OpenAI API key cannot be empty."
        )

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=MODEL_TEMPERATURE,
        max_tokens=MAX_OUTPUT_TOKENS,
        api_key=api_key,
    )

    return llm


# ============================================================
# CREATE LLMCHAIN
# ============================================================

def create_assessment_chain(api_key):
    """
    Create a reusable LLMChain for medical assessment.

    Args:
        api_key (str):
            User-provided OpenAI API key.

    Returns:
        LLMChain:
            Reusable assessment chain.
    """

    llm = create_llm(api_key)

    chain = LLMChain(
        llm=llm,
        prompt=ASSESSMENT_CHAT_TEMPLATE,
        verbose=False,
    )

    return chain


# ============================================================
# PATIENT ASSESSMENT
# ============================================================

def assess_patient(
    patient_data,
    api_key,
    cache_enabled=True,
    cache_type="InMemoryCache",
):
    """
    Assess patient information using the user's OpenAI API key.

    Args:
        patient_data (dict):
            Patient information.

        api_key (str):
            User-provided OpenAI API key.

        cache_enabled (bool):
            Whether caching is enabled.

        cache_type (str):
            Selected cache type.

    Returns:
        dict:
            Safely parsed JSON assessment.
    """

    # Import here to avoid circular imports
    from src.cache_manager import (
        set_cache,
        disable_cache,
    )

    # --------------------------------------------------------
    # Configure cache
    # --------------------------------------------------------

    if cache_enabled:

        # Public version only supports InMemoryCache.
        set_cache("InMemoryCache")

    else:

        disable_cache()

    # --------------------------------------------------------
    # Create chain
    # --------------------------------------------------------

    chain = create_assessment_chain(
        api_key
    )

    # --------------------------------------------------------
    # Run LLMChain
    # --------------------------------------------------------

    response = chain.invoke(
        patient_data
    )

    # --------------------------------------------------------
    # Extract model text
    # --------------------------------------------------------

    if isinstance(response, dict):

        raw_output = response.get(
            "text",
            "",
        )

    else:

        raw_output = str(response)

    # --------------------------------------------------------
    # Parse JSON safely
    # --------------------------------------------------------

    result = safe_json_parse(
        raw_output
    )

    return result


# ============================================================
# STREAMING NARRATIVE
# ============================================================

def stream_narrative(
    patient_data,
    api_key,
):
    """
    Stream a human-readable medical guidance narrative.

    The user's API key is supplied at runtime.

    Args:
        patient_data (dict):
            Patient information.

        api_key (str):
            User-provided OpenAI API key.

    Yields:
        str:
            Individual chunks of generated text.
    """

    # --------------------------------------------------------
    # Create LLM using user's API key
    # --------------------------------------------------------

    llm = create_llm(
        api_key
    )

    # --------------------------------------------------------
    # Format chat messages
    # --------------------------------------------------------

    messages = NARRATIVE_CHAT_TEMPLATE.format_messages(
        **patient_data
    )

    # --------------------------------------------------------
    # Stream response
    # --------------------------------------------------------

    for chunk in llm.stream(
        messages
    ):

        if chunk.content:

            yield chunk.content


# ============================================================
# SYSTEM / HUMAN / AI MESSAGE DEMO
# ============================================================

def message_demo():
    """
    Demonstrate SystemMessage, HumanMessage and AIMessage.

    This function is included to satisfy the assignment
    requirement for working directly with LangChain messages.

    Returns:
        dict:
            Demonstration conversation.
    """

    system_message = SystemMessage(
        content=SYSTEM_PROMPT
    )

    human_message = HumanMessage(
        content=(
            "I have a mild headache and runny nose. "
            "Please provide general educational information."
        )
    )

    ai_message = AIMessage(
        content=(
            "These symptoms can have several possible causes. "
            "This information is educational only and does not "
            "represent a confirmed diagnosis. Consider consulting "
            "a qualified healthcare professional if symptoms "
            "persist or worsen."
        )
    )

    return {
        "system_message": system_message,
        "human_message": human_message,
        "ai_message": ai_message,
    }


# ============================================================
# DIRECT MESSAGE CONVERSATION
# ============================================================

def run_message_conversation(
    user_question,
    api_key,
):
    """
    Send a direct SystemMessage + HumanMessage conversation
    using the user's OpenAI API key.

    Args:
        user_question (str):
            User's question.

        api_key (str):
            User-provided OpenAI API key.

    Returns:
        str:
            AI response.
    """

    llm = create_llm(
        api_key
    )

    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT
        ),
        HumanMessage(
            content=user_question
        ),
    ]

    response = llm.invoke(
        messages
    )

    return response.content


# ============================================================
# TEST JSON OUTPUT
# ============================================================

def validate_assessment_result(
    result
):
    """
    Check that the assessment contains the required fields.

    Args:
        result (dict):
            Parsed assessment result.

    Returns:
        bool:
            True if the required structure exists.
    """

    required_fields = [
        "summary",
        "possible_conditions",
        "urgency_level",
        "recommended_next_steps",
        "questions_for_doctor",
        "warning_signs",
    ]

    if not isinstance(
        result,
        dict,
    ):
        return False

    for field in required_fields:

        if field not in result:

            return False

    return True