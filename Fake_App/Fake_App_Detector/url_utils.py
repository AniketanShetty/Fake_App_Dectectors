# url_utils.py

import re

def extract_package_from_url(url: str) -> str | None:
    """
    Extracts package name from a Play Store URL.
    Example:
    https://play.google.com/store/apps/details?id=com.phonepe.app
    → com.phonepe.app
    """
    if not url:
        return None

    # Standard Play Store pattern
    match = re.search(r"[?&]id=([a-zA-Z0-9._]+)", url)
    if match:
        return match.group(1)

    return None
