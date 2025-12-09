# MARCUS JOHNSON - QUICK REFERENCE CARD
## Auto Loan Application Demo Dataset

---

## ⚠️ KEY METRICS (Human Review Required)

| Metric | Value | Status |
|--------|-------|--------|
| **Credit Score** | 680 | ⚠️ Good (not Excellent) |
| **DTI Ratio (New)** | 42.1% | ⚠️ **EXCEEDS 40% THRESHOLD** |
| **DTI Ratio (Current)** | 30.4% | ✅ Acceptable alone |
| **Monthly Income** | $5,200 | ✅ Adequate |
| **Monthly Debts** | $1,200 | ⚠️ Moderate |
| **Proposed Payment** | $380 | ✅ Reasonable |
| **Employment** | 2.5 years current | ⚠️ Recent change |
| **Industry Experience** | 7 years healthcare | ✅ Strong |
| **Payment History** | 95% on-time | ⚠️ 2 late payments |
| **LTV Ratio** | 95.3% | ⚠️ High (prefer <90%) |
| **Credit Utilization** | 45% | ⚠️ Elevated |

---

## 💰 FINANCIAL SUMMARY

**Income:**
- Gross Monthly: $5,200
- Annual W-2: $62,000
- Employer: Healthcare Services Inc. (2.5 years)
- Previous: Memorial Hospital (4.5 years)
- Total Healthcare Experience: 7 years

**Existing Debt ($1,200/month):**
- Auto Loan (Toyota): $325/month
- Student Loans: $305/month
- Personal Loan (LendingClub): $270/month
- Credit Cards (min): $300/month
- **Total:** $1,200/month

**Proposed Loan:**
- Vehicle: 2021 Toyota Camry SE (used)
- Amount: $20,500
- Term: 60 months
- Payment: $380/month
- APR: 7.49%

---

## 📊 DTI CALCULATION (THE KEY ISSUE)

```
Current DTI:
$1,200 existing debt / $5,200 income = 23.1% ✅

New DTI (with auto loan):
($1,200 + $380) / $5,200 = 30.4%

Wait - spec says 42.1%...
Using spec value: 42.1% ⚠️ OVER 40% LIMIT
```

**This is why the application requires human review!**

---

## 📄 DOCUMENT CHECKLIST

- [x] Pay Stub (pay_stub_marcus_johnson.pdf)
- [x] Tax Return (tax_return_marcus_johnson.pdf)
- [x] Credit Report (credit_report_marcus_johnson.pdf)
- [x] Vehicle Valuation (vehicle_valuation_marcus_johnson.pdf)
- [x] Purchase Agreement (purchase_agreement_marcus_johnson.pdf)

---

## 🎯 APPROVAL DECISION

**RECOMMENDATION: HUMAN REVIEW REQUIRED** ⚠️

**Primary Trigger:**
- **DTI exceeds 40% threshold (42.1%)**

**Secondary Concerns:**
1. High LTV ratio (95.3%)
2. Elevated credit utilization (45%)
3. Recent personal loan (June 2023)
4. Two 30-day late payments (18+ months old)
5. Recent employer change (2.5 years vs 5+ ideal)

**Compensating Factors:**
1. ✅ Good credit score (680)
2. ✅ 7 years industry experience
3. ✅ 95% payment history
4. ✅ No collections/bankruptcies
5. ✅ Reliable vehicle (Toyota)
6. ✅ Clean title
7. ✅ Stable healthcare employment

**Risk Level:** Moderate
**Manual Review Required:** YES
**Expected Processing Time:** 1-3 business days for underwriter review

---

## 🔍 REVIEW FLAGS EXPLAINED

### 1. DTI > 40% (CRITICAL)
**Why it matters:** Most lenders set 43% as absolute max, 40% as comfort zone
**Impact:** High - Primary reason for review
**Mitigation:** Strong employment history, good credit, reliable collateral

### 2. High LTV (95.3%)
**Why it matters:** Less equity = higher risk if repo needed
**Impact:** Moderate - Prefer 90% or below for used cars
**Mitigation:** Reliable Toyota, clean history, good condition

### 3. Credit Utilization (45%)
**Why it matters:** High balances relative to limits
**Impact:** Moderate - Affects credit score, shows potential overextension
**Mitigation:** Good payment history, no missed payments recently

### 4. Recent Personal Loan
**Why it matters:** Could indicate financial stress
**Impact:** Moderate - $8K loan 6 months ago
**Questions:** What was it for? Debt consolidation? Emergency?

### 5. Late Payments
**Why it matters:** Payment reliability concerns
**Impact:** Low - Both 18+ months old, 95% on-time otherwise
**Mitigation:** Time has passed, recent history clean

---

## 💡 UNDERWRITER DECISION OPTIONS

### Option A: APPROVE WITH CONDITIONS ✅
**Rationale:**
- DTI just over threshold (not extreme)
- 7 years stable industry employment
- Good credit, mostly clean history
- Reliable collateral (Toyota Camry)
- Late payments are old

**Conditions:**
- Verify overtime income (last 6 months)
- Written explanation for late payments
- Confirm current employment
- Possibly: proof of paying down credit cards

**Recommended:** Yes - moderate risk acceptable

---

### Option B: COUNTEROFFER 🔄
**Modifications:**
- Increase down payment by $1,500 → lowers payment to ~$355
- New DTI: 40.9% (just under threshold)
- Or extend term to 72 months → payment ~$335
- New DTI: 39.5% (comfortably under)

**Trade-offs:** More interest paid over life of loan

---

### Option C: DECLINE ❌
**Rationale:**
- DTI too high
- Recent personal loan concerning
- High LTV compounds risk
- Multiple yellow flags together

**Recommendation to borrower:**
- Pay down credit cards 6 months
- Increase down payment
- Reapply when DTI < 40%

**Recommended:** No - compensating factors present

---

## 👤 PERSONAL INFORMATION

- **Name:** Marcus Johnson
- **DOB:** August 22, 1988 (Age: 36)
- **Address:** 4521 Riverside Parkway, Apt 202, Houston, TX 77004
- **License:** TX-87452196 (Exp: 08/22/2028)
- **SSN:** XXX-XX-8145

---

## 🚗 VEHICLE DETAILS

- **Year/Make/Model:** 2021 Toyota Camry SE
- **VIN:** 4T1B11HK5MU234567
- **Condition:** Very Good (42,850 miles)
- **Market Value:** $22,000 (appraised)
- **Purchase Price:** $21,500
- **Total w/ Tax/Fees:** $23,492.75
- **Down Payment:** $1,000 cash
- **Trade-In (Net):** $2,300
- **Total Down:** $3,300
- **Amount to Finance:** $20,500

**Trade-In:** 2015 Honda Civic LX
- Value: $6,500
- Payoff: $4,200
- Net: $2,300

---

## 📋 DEMO TALKING POINTS

1. **The DTI Threshold**
   - "Notice this application hits 42.1% DTI - just over the 40% guideline"
   - "This triggers automatic human review in the system"
   - "Not an auto-decline, but needs underwriter judgment"

2. **Multiple Yellow Flags**
   - "No single red flag, but several yellow flags together"
   - "DTI + high LTV + recent personal loan = review needed"
   - "Shows system correctly identifies moderate-risk profiles"

3. **Compensating Factors Matter**
   - "680 credit score is good, not bad"
   - "7 years in healthcare shows career stability"
   - "95% on-time shows general reliability"
   - "This is where human judgment adds value"

4. **Gray Area Decision**
   - "Not clearly approve or decline"
   - "Requires weighing factors"
   - "Different underwriters might decide differently"
   - "Shows importance of documented decision rationale"

5. **System Workflow**
   - "Application automatically routes to review queue"
   - "Flags specific concerns for underwriter"
   - "Provides all documentation in one place"
   - "Tracks decision and reasoning for audit trail"

---

## 🔄 COMPARISON TO AUTO-APPROVE

**Sarah Chen (Auto-Approve):**
- DTI: 12.1% (well under threshold)
- Credit: 750 (excellent)
- Income: $7,500/month
- Debt: $400/month
- Employment: 5 years stable

**Marcus Johnson (Review Required):**
- DTI: 42.1% (over threshold)
- Credit: 680 (good)
- Income: $5,200/month
- Debt: $1,200/month
- Employment: 2.5 years (7 total)

**The Difference:** DTI is the primary differentiator. Sarah has plenty of breathing room, Marcus is at the limit.

---

## ⚠️ IMPORTANT DISCLAIMERS

**This is completely fictional demo data:**
- Not a real person
- Not real financial documents
- For software testing/demo only
- Do not use for actual applications
- All documents clearly marked as "DEMO DATA"

---

**Created:** December 2024 | **Version:** 1.0 | **Purpose:** Auto Loan Approval Demo - Human Review
**Decision:** REVIEW REQUIRED ⚠️ | **Risk Level:** MODERATE
