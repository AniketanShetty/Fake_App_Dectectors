import json
from data import CANDIDATE_APPS
from features import (
    name_similarity,
    package_similarity,
    publisher_match,
    text_suspicion_score,
    permission_suspicion_score,
)
from scoring import risk_score

def get_results():
    results = []

    for app in CANDIDATE_APPS:
        name_sim = name_similarity(app)
        pkg_sim = package_similarity(app)
        pub_ok = publisher_match(app)
        text_score = text_suspicion_score(app)
        perm_score = permission_suspicion_score(app)
        risk = risk_score(app)

        reasons = [
            f"Name similarity with official PhonePe app: {name_sim}",
            f"Package name similarity with official PhonePe app: {pkg_sim}",
            f"Text suspicion score (keywords): {text_score}",
            f"Permission suspicion score: {perm_score}",
        ]
        if pub_ok:
            reasons.append("Publisher matches official PhonePe publisher")
        else:
            reasons.append("Publisher does NOT match official PhonePe publisher")

        results.append({
            "appName": app["name"],
            "packageId": app["package"],
            "risk": risk,
            "reason": reasons,
        })

    # Sort apps by risk (highest first) for nicer display
    results_sorted = sorted(results, key=lambda r: r["risk"], reverse=True)
    return {"results": results_sorted}


def main():
    print("Running backend...\n")
    output = get_results()
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
