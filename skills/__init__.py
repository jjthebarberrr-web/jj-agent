"""Skills system for reusable scaffolding templates."""

from .fastapi import get_fastapi_skill

SKILLS = {
    "fastapi": get_fastapi_skill,
}


def get_skill(name: str):
    """Get a skill by name."""
    if name in SKILLS:
        return SKILLS[name]()
    return None


def list_skills():
    """List all available skills."""
    return list(SKILLS.keys())
