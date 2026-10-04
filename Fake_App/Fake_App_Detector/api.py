# api.py - Flask backend for Fake App Detector

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from data import CANDIDATE_APPS
from scoring import risk_score
from features import (
    name_similarity,
    package_similarity,
    text_suspicion_score,
    permission_suspicion_score,
    publisher_match,
)
from url_utils import extract_package_from_url

app = Flask(__name__)
CORS(app)  # allow requests from your frontend (Live Server / React, etc.)


def build_result_item(app_dict: dict) -> dict:
    """
    Build one result row for an app, in the exact format
    your frontend table expects.
    """
    name_sim = name_similarity(app_dict)
    pkg_sim = package_similarity(app_dict)
    text_score = text_suspicion_score(app_dict)
    perm_score = permission_suspicion_score(app_dict)
    pub_match = publisher_match(app_dict)
    risk = risk_score(app_dict)

    reasons = [
        f"Name similarity with official PhonePe app: {name_sim}",
        f"Package name similarity with official PhonePe app: {pkg_sim:.2f}",
        f"Text suspicion score (keywords): {text_score}",
        f"Permission suspicion score: {perm_score}",
        (
            "Publisher matches official PhonePe publisher"
            if pub_match
            else "Publisher does NOT match official PhonePe publisher"
        ),
    ]

    return {
        "appName": app_dict["name"],
        "packageId": app_dict["package"],
        "risk": round(risk, 2),
        "reason": reasons,
    }


@app.route("/api/apps", methods=["GET"])
def api_apps():
    """
    Return risk info for all sample apps.
    Used by the 'Scan Apps' button on the frontend.
    """
    results = [build_result_item(a) for a in CANDIDATE_APPS]
    # Sort by risk descending so most suspicious appear first
    results = sorted(results, key=lambda r: r["risk"], reverse=True)
    return jsonify({"results": results})


@app.route("/api/check-url", methods=["POST"])
def api_check_url():
    """
    Check a single Play Store URL.

    Request JSON:
      { "url": "https://play.google.com/store/apps/details?id=com.phonepe.app" }

    Response JSON:
      {
        ok: true/false,
        url: "...",
        packageId: "...",
        found: true/false,
        risk: number,
        reason: [ ... ],
        appName: "..."
      }
    """
    data = request.get_json(force=True) or {}
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"ok": False, "error": "No URL provided"}), 400

    package_id = extract_package_from_url(url)
    if not package_id:
        return jsonify(
            {
                "ok": False,
                "url": url,
                "packageId": None,
                "found": False,
                "risk": 0,
                "reason": [
                    "Could not extract package ID from URL. "
                    "Expected a Play Store link with ?id=<package>."
                ],
            }
        )

    # Look up in our sample dataset
    app_obj = next(
        (a for a in CANDIDATE_APPS if a["package"] == package_id), None
    )

    if app_obj is None:
        # Not in our toy dataset – be honest about limitation
        return jsonify(
            {
                "ok": False,
                "url": url,
                "packageId": package_id,
                "found": False,
                "risk": 0,
                "reason": [
                    "Package not present in our sample dataset "
                    "(academic prototype – cannot classify unknown apps)."
                ],
            }
        )

    # We have this app in our dataset – compute full evidence
    item = build_result_item(app_obj)

    return jsonify(
        {
            "ok": True,
            "url": url,
            "packageId": package_id,
            "found": True,
            "risk": item["risk"],
            "reason": item["reason"],
            "appName": item["appName"],
        }
    )


@app.route("/health", methods=["GET"])
def health():
    """
    Simple health endpoint (optional).
    Can be used by frontend to check if backend is up.
    """
    return jsonify(
        {
            "status": "ok",
            "service": "fake_app_scanner",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )


if __name__ == "__main__":
    # Run on 0.0.0.0 so it's reachable from browser on same machine
    app.run(host="0.0.0.0", port=5000, debug=True)
