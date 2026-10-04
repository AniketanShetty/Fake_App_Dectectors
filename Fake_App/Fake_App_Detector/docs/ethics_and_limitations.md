# Ethics & Limitations

## Do No Harm

- We do **not** execute real malware.
- We use a small **curated dataset** of apps defined in `data.py`, including:
  - Official apps (PhonePe, GPay, BHIM).
  - Synthetic fake / suspect apps created for demonstration.
- We do not collect or process any **user** data.

## No Abusive Scraping

- In this hackathon prototype, we **do not** scrape the Google Play Store directly.
- The "Fetch" step is mocked:
  - Apps are loaded from `data.py`.
  - For URL tests, we only parse the package id and then look it up in our dataset.

## Privacy

- We work only with app-level metadata:
  - Name
  - Package id
  - Publisher
  - Description
  - Permissions
- No personal identifiers, no phone numbers, no messages.

## Prototype, Not Production

- This is an **academic prototype** built for BMSCE hackathon.
- The risk scoring is heuristic and based on a tiny dataset.
- It should **not** be used as a production security product without:
  - Larger datasets.
  - Robust evaluation.
  - Legal + compliance review.

## Limitations

- Limited dataset: only a handful of curated apps.
- No real-time integration with Play Store / APK mirrors.
- Detection is focused on PhonePe; not generalized to all financial apps.
- Rule-based scoring; not yet using large-scale ML.
