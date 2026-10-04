# Threat Model

## Attacker

- Fraudsters / scammers who publish fake or lookalike PhonePe apps on the Google Play Store.
- Their goal is to:
  - Trick users into installing the fake app.
  - Steal UPI PINs, OTPs, or other sensitive information.
  - Redirect payments or harvest personal data.

## Victim

- End users who install fake PhonePe apps and enter sensitive data.
- The PhonePe brand:
  - Reputation damage.
  - Increased support load and user complaints.
  - Potential financial liabilities / chargebacks.

## Assets at Risk

- User’s UPI credentials and bank details.
- Integrity of PhonePe’s brand and user trust.
- Security of UPI transactions.

## Attacker Capabilities

- Publishing apps to the Google Play Store under arbitrary developer accounts.
- Reusing PhonePe-like names, icons, and descriptions.
- Requesting sensitive permissions (SMS, contacts, call logs).

## Our Detection Focus

- Apps on the Play Store that:
  - Have PhonePe-like names or packages.
  - Use scammy marketing descriptions (free money, bonus, tricks).
  - Request suspicious combinations of permissions.
  - Are published by non-official developers.

## Out of Scope

- Malware distributed only via sideloaded APKs (not on Play Store).
- Overlay attacks on top of the real PhonePe app.
- Web or SMS-based phishing links.
- Full dynamic malware analysis / sandboxing.

Our system focuses specifically on **brand impersonation risk** for PhonePe apps on Play Store.
