# Fake PhonePe App Detector – BMSCE Hackathon

## 1. Problem

Fake and lookalike apps on the Google Play Store can impersonate payment apps like PhonePe, 
trick users into entering UPI PINs/OTPs, and steal money or damage brand reputation.

Goal: Given a **Google Play Store URL** or a **set of candidate apps** for the brand PhonePe, 
our backend assigns a **risk score (0–100)** and explains *why* an app looks suspicious 
(name, package, publisher, keywords, permissions). It also generates an **evidence kit** 
and a **takedown email template** for reporting to Google.

---

## 2. Scope

- Platform: **Android (Google Play Store)**
- Brand: **PhonePe**
- Domain: **UPI / digital payments**
- Threats covered:
  - Fake / lookalike apps using the PhonePe name or branding
  - Typosquatted package names (e.g., `com.ph0nepe.upi`)
  - Reward / cashback / bonus / “trick” apps pretending to be related to PhonePe
- Out of scope:
  - iOS App Store
  - Sideloaded APK malware
  - Web/SMS phishing, overlay attacks

(See `docs/scope.md` for more details.)

---

## 3. Project structure

```text
Fake_App_Detector/
  data.py               # Official PhonePe + curated candidate apps
  features.py           # Feature extractors (name, package, publisher, text, permissions)
  scoring.py            # risk_score(app) -> 0–100
  main.py               # Batch scoring of all candidate apps (for frontend)
  url_utils.py          # Parse package id from Google Play URL
  url_checker.py        # Check a single URL -> risk + reasons
  labels.py             # Ground-truth labels (genuine vs fake)
  metrics.py            # Confusion matrix, precision, recall
  report.py             # Evidence builder + takedown email generator
  demo_evidence.py      # Demo: show evidence + email for most suspicious app
  docs/
    scope.md
    data_and_signals.md
    threat_model.md
    ethics_and_limitations.md
  icons/                # App icons (mocked) for evidence (if needed)
