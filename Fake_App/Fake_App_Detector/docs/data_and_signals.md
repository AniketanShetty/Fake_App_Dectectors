# Data & Signals

## Candidate Apps

For the hackathon prototype, we use a **small curated dataset** defined in `data.py`:

- Official PhonePe app
- Other genuine UPI apps:
  - Google Pay
  - BHIM
- Synthetic fake / suspect apps:
  - “PhonePe Bonus Money Trick”
  - “PhonePay Cashback Offer 2025”
  - “PhonePe Free Cashback Pro”
  - etc.

These apps are representative examples for demonstrating the detection pipeline.

## Ground Truth Labels

Ground truth is defined in `labels.py`:

- `0` = genuine app
- `1` = fake / suspect app

Examples:

- `com.phonepe.app` → 0 (genuine)
- `com.google.android.apps.nbu.paisa.user` → 0 (genuine GPay)
- `in.org.npci.upiapp` → 0 (genuine BHIM)
- `com.phonepe.bonus.trick2025` → 1 (suspect)
- `com.phonepay.cashback2025.free` → 1 (suspect)

This allows us to compute a confusion matrix and precision/recall.

## Signals Used

All features are implemented in `features.py`:

1. **Name similarity**  
   - Fuzzy string match between candidate name and official PhonePe name.
   - Example: “PhonePe: UPI, Payment, Recharge” vs “PhonePe Bonus Money Trick”

2. **Package similarity**  
   - String similarity between candidate package and `com.phonepe.app`.
   - Detects typosquats such as `com.ph0nepe.upi`.

3. **Publisher match**  
   - Exact comparison between candidate publisher and `PhonePe Pvt. Ltd`.
   - Publisher mismatch is a strong signal of impersonation.

4. **Text suspicion score**  
   - Score based on presence of scammy keywords in the description:
     - `free`, `bonus`, `earn`, `reward`, `cashback`, `double money`, `lottery`, `trick`, `hack`, `win`, `prize`.

5. **Permission suspicion score**  
   - Score based on dangerous permissions:
     - `READ_SMS`, `READ_CONTACTS`, `READ_CALL_LOG`, `WRITE_SMS`.

These signals are combined by `risk_score(app)` in `scoring.py` to produce a final risk score between 0 and 100.
