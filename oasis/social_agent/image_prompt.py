"""
Image Generation System Prompt for Facebook/Instagram Quality Photos (Phase 3B)

This module provides the base system prompt and utilities for generating
high-quality social media image prompts that produce realistic, authentic-looking
photos suitable for Facebook/Instagram feeds.
"""

# Base system prompt prepended to all image generation requests
# Designed to produce Instagram/Facebook-quality photos
IMAGE_SYSTEM_PROMPT = """You are generating an image prompt for a realistic social media photo.

Style requirements:
- Modern smartphone photography aesthetic (iPhone/Samsung quality)
- Natural lighting preferred, golden hour when relevant
- Candid, authentic feel - not overly staged or stock-photo-like
- High resolution, sharp focus on subject
- Realistic colors, not oversaturated
- Appropriate for Instagram/Facebook content

Composition guidelines:
- Rule of thirds when appropriate
- Clean backgrounds that don't distract
- Proper depth of field for the subject matter
- Eye-level or slightly elevated angles for portraits

DO NOT include:
- Watermarks or text overlays
- Artificial lens flares or heavy filters
- Unrealistic proportions or AI artifacts
- Celebrity likenesses or copyrighted characters
"""


def build_image_prompt(user_prompt: str) -> str:
    """
    Combine the system prompt style guidance with a user's image description.

    This function prepends the IMAGE_SYSTEM_PROMPT to ensure consistent,
    high-quality social media photo generation across all image requests.

    Args:
        user_prompt: The agent's description of what they want in the image
            (e.g., "A homemade pasta dish on a rustic wooden table")

    Returns:
        Full prompt ready for image generation API, combining style guidance
        with the specific subject matter.

    Example:
        >>> prompt = build_image_prompt("Sunset over the ocean with waves")
        >>> # Returns IMAGE_SYSTEM_PROMPT + "\\n\\nSubject: Sunset over the ocean with waves"
    """
    return f"{IMAGE_SYSTEM_PROMPT}\n\nSubject: {user_prompt}"

