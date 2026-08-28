"""
MediGuide AI - Cache Manager

Public Deployment Version

This file uses only InMemoryCache.

Why?
- InMemoryCache stores responses temporarily in RAM.
- Data is lost when the application restarts.
- No persistent SQLite database is created.
- Better suited for a public educational prototype.
- API keys are NOT stored in the cache.
"""

from langchain_core.globals import set_llm_cache
from langchain_community.cache import InMemoryCache


# ============================================================
# CACHE STATE
# ============================================================

_current_cache_type = None


# ============================================================
# CREATE IN-MEMORY CACHE
# ============================================================

def create_memory_cache():
    """
    Create an InMemoryCache instance.

    Returns:
        InMemoryCache:
            Memory-based LangChain cache.
    """

    return InMemoryCache()


# ============================================================
# SET CACHE
# ============================================================

def set_cache(cache_type="InMemoryCache"):
    """
    Enable the selected cache.

    Public deployment supports only InMemoryCache.

    Args:
        cache_type (str):
            Cache type. Only "InMemoryCache" is supported.

    Returns:
        str:
            Name of the active cache.
    """

    global _current_cache_type

    # --------------------------------------------------------
    # Only allow InMemoryCache
    # --------------------------------------------------------

    if cache_type != "InMemoryCache":

        raise ValueError(
            "Only InMemoryCache is supported in the public version."
        )

    # --------------------------------------------------------
    # Create memory cache
    # --------------------------------------------------------

    cache = create_memory_cache()

    # --------------------------------------------------------
    # Register cache globally
    # --------------------------------------------------------

    set_llm_cache(cache)

    _current_cache_type = "InMemoryCache"

    return _current_cache_type


# ============================================================
# DISABLE CACHE
# ============================================================

def disable_cache():
    """
    Disable LangChain's global LLM cache.

    This is useful when privacy is preferred and
    responses should not be cached.
    """

    global _current_cache_type

    set_llm_cache(None)

    _current_cache_type = None


# ============================================================
# GET CURRENT CACHE TYPE
# ============================================================

def get_current_cache():
    """
    Return the currently selected cache type.

    Returns:
        str or None:
            Current cache type.
    """

    return _current_cache_type


# ============================================================
# CACHE DESCRIPTION
# ============================================================

def get_cache_description(cache_type):
    """
    Return a beginner-friendly explanation of the cache.
    """

    descriptions = {

        "InMemoryCache": (
            "InMemoryCache stores LLM responses temporarily "
            "in application memory. It is fast and does not "
            "create a persistent database file. Cached data "
            "is lost when the application restarts."
        ),

    }

    return descriptions.get(
        cache_type,
        "No cache selected.",
    )


# ============================================================
# CACHE COMPARISON
# ============================================================

def get_cache_comparison():
    """
    Return cache information for README or UI.
    """

    return {

        "InMemoryCache": {
            "stored_in": "RAM (memory)",
            "speed": "Fast",
            "survives_restart": "No",
            "persistent_database": "No",
            "best_for": "Temporary session-based caching",
        },

    }