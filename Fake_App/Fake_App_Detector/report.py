from data import OFFICIAL_APP
from official_meta import OFFICIAL_PHONEPE_META
from features import (
    name_similarity,
    package_similarity,
    publisher_match,
    text_suspicion_score,
    permission_suspicion_score,
)
from scoring import risk_score


def build_evidence(app: dict) -> dict:
    """
    Build an evidence object for a candidate app, enriched with official PhonePe metadata.

    This is what you show in:
    - Evidence JSON in demo_evidence.py
    - PDF / slides as your "Evidence Kit" output
    """

    scores = {
        "name_similarity": name_similarity(app),
        "package_similarity": package_similarity(app),
        "publisher_match": publisher_match(app),
        "text_suspicion": text_suspicion_score(app),
        "permission_suspicion": permission_suspicion_score(app),
        "risk_score": risk_score(app),
    }

    evidence = {
        # Official reference information for the genuine PhonePe app
        "official": {
            "app_name": OFFICIAL_APP["name"],
            "package_name": OFFICIAL_APP["package"],
            "publisher": OFFICIAL_APP["publisher"],
            "icon_phash": OFFICIAL_PHONEPE_META.get("icon_phash"),
            "icon_sha256": OFFICIAL_PHONEPE_META.get("icon_sha256"),
            "trusted_file_names": OFFICIAL_PHONEPE_META.get("trusted_file_names", []),
            "trusted_labels": OFFICIAL_PHONEPE_META.get("trusted_labels", []),
            "notes": OFFICIAL_PHONEPE_META.get("notes", ""),
        },

        # Candidate app details (what we are suspicious about)
        "candidate": {
            "app_name": app["name"],
            "package_name": app["package"],
            "publisher": app["publisher"],
            "icon_path": app.get("icon_path"),
            "description": app.get("description"),
            "permissions": app.get("permissions", []),
        },

        # All the numeric scores used in risk calculation
        "scores": scores,
    }

    return evidence


def generate_takedown_email(evidence: dict) -> str:
    """
    Generate a human-readable takedown email using the evidence object.

    Assumes evidence structure from build_evidence().
    """

    cand = evidence["candidate"]
    scores = evidence["scores"]

    app_name = cand["app_name"]
    package = cand["package_name"]
    publisher = cand["publisher"]

    return f"""
To: Google Play Support
Subject: Urgent takedown request – Fake app impersonating PhonePe

Dear Google Play Team,

We have identified a suspicious app that appears to be impersonating the official PhonePe application.

App details:
- Name: {app_name}
- Package: {package}
- Publisher: {publisher}

Automated analysis (vs official PhonePe app):
- Name similarity: {scores['name_similarity']:.2f}
- Package similarity: {scores['package_similarity']:.2f}
- Publisher match: {scores['publisher_match']}
- Text suspicion score (scammy keywords): {scores['text_suspicion']:.2f}
- Permission suspicion score (dangerous permissions): {scores['permission_suspicion']:.2f}
- Overall risk score (0–100): {scores['risk_score']:.2f}

This analysis is based on our academic prototype for detecting fake apps impersonating financial brands, 
using the official PhonePe metadata (package name, trusted labels, and icon signatures) as reference.

Based on these signals, we believe this app may mislead users and could be used for fraud.

Regards,
[Aniketan Shetty, N.M. Vijeyendranath, Sangamesh Nidode]
[BMS College of Engineering]
"""
