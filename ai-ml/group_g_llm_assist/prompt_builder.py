"""
Group G: Grounded Investigation Prompt Builder.
Constructs strict prompts constraining LLM reasoning to cited observation IDs.
"""

from typing import List, Dict, Any

SYSTEM_INSTRUCTION = (
    "You are an investigative assistant analyzing cyber intelligence observations. "
    "CRITICAL CONSTRAINT: You must only draw conclusions strictly supported by the provided observations. "
    "Every factual assertion or linking hypothesis MUST explicitly cite the supporting observation ID in brackets, e.g. [OBS-1]. "
    "Do NOT introduce external knowledge, ungrounded assumptions, or authoritative merge decisions."
)


def build_investigation_prompt(
    subject_a: str,
    subject_b: str,
    observations: List[Dict[str, Any]],
) -> Dict[str, str]:
    """
    Format evidence observations with distinct observation IDs into a structured prompt.
    Returns: {"system": str, "user": str, "observation_ids": list[str]}
    """
    obs_lines = []
    valid_ids = []

    for idx, obs in enumerate(observations, 1):
        obs_id = obs.get("id", f"OBS-{idx}")
        family = obs.get("family", "UNKNOWN")
        desc = obs.get("description", obs.get("extra", ""))
        obs_lines.append(f"[{obs_id}] Family: {family} | Details: {desc}")
        valid_ids.append(obs_id)

    obs_block = "\n".join(obs_lines) if obs_lines else "No observations provided."

    user_prompt = (
        f"Analyze potential connections between Subject A ({subject_a}) and Subject B ({subject_b}).\n\n"
        f"Available Observations:\n{obs_block}\n\n"
        f"Task:\n"
        f"1. Summarize verifiable corroboration with explicit citations.\n"
        f"2. Propose non-authoritative linking hypotheses supported by cited observation IDs.\n"
        f"3. Note any conflicting signals or gaps."
    )

    return {
        "system": SYSTEM_INSTRUCTION,
        "user": user_prompt,
        "valid_ids": valid_ids,
    }
