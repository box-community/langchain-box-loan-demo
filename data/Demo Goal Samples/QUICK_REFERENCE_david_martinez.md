# DAVID MARTINEZ - QUICK REFERENCE CARD
## Auto Loan Application Demo Dataset

---

## 🚨 KEY METRICS (Regional Director Escalation Required)

| Metric | Value | Status | Violation Level |
|--------|-------|--------|-----------------|
| **DTI Ratio (New)** | **47.0%** | 🚨 **EXCEEDS 43% HARD LIMIT** | **MODERATE** |
| **Credit Score** | 640 | 🚨 **20 pts above minimum (620)** | **MINOR** |
| **LTV Ratio** | 107.1% | ⚠️ Near max (110%) | High Risk |
| **Monthly Income** | $4,800 (conservative) | ⚠️ Variable | Concern |
| **Monthly Debts** | $1,600 | 🚨 High | Issue |
| **Proposed Payment** | $640 | 🚨 Very High | Issue |
| **Employment** | 18 months | ⚠️ Short tenure | Concern |
| **Loan Term** | 72 months | ⚠️ Maximum | Extended Risk |

**Decision:** 🚨 **REGIONAL DIRECTOR ESCALATION REQUIRED**

**Reason:** 2 MODERATE/MINOR VIOLATIONS = Requires higher authority approval

---

## 🚨 VIOLATION SUMMARY

### MODERATE VIOLATION #1: DTI EXCEEDS 43%
- **Current DTI:** 33.3% ($1,600 / $4,800)
- **New DTI:** **47.0%** ($2,240 / $4,800)
- **Threshold:** 43% (hard limit)
- **Severity:** MODERATE - Requires Regional Director approval

### MINOR VIOLATION #2: Credit Near Minimum
- **Credit Score:** 640
- **Minimum Threshold:** 620
- **Buffer:** Only 20 points
- **Severity:** MINOR - But concerning with recent late payment

### HIGH RISK FACTORS (Not violations, but significant):
- ⚠️ LTV 107.1% (near 110% max)
- ⚠️ Negative equity rollover ($2,000)
- ⚠️ 72-month term (maximum)
- ⚠️ Variable construction income
- ⚠️ Short employment (18 months)
- ⚠️ 72% credit utilization
- ⚠️ Recent 30-day late payment (Nov 2024)

---

## 💰 FINANCIAL SUMMARY

**Income (Variable):**
- Current bi-weekly: $2,735
- 6-month average: $2,533
- **Conservative monthly: $4,800** (base only, no OT)
- Annual: ~$57,600
- Employer: Southwest Construction Co. (18 months)
- Industry: Construction (4+ years total)

**Existing Debt ($1,600/month):**
- Auto Loan: $425/month
- Personal Loans: $525/month ($275 + $250)
- Medical Installment: $180/month
- Credit Cards (min): $470/month
- **Total:** $1,600/month

**Proposed Loan:**
- Vehicle: 2019 Ford F-150 XLT
- Amount: $30,000 (includes $2K neg equity)
- Term: 72 months (maximum)
- Payment: $640/month
- APR: 14.99% (subprime)

---

## 📊 CRITICAL DTI CALCULATION

```
Current Debt: $1,600/month
Income: $4,800/month
Current DTI: $1,600 / $4,800 = 33.3% ✅

New Payment: $640/month
Less: Trade payoff: -$425/month
Net New Debt: +$215/month

Wait, that would be 37.8% total...

Let me recalculate properly:
Total New Debt: $1,600 + $640 = $2,240
New DTI: $2,240 / $4,800 = 46.7% ≈ 47%

BUT - we're paying off the $425 trade loan
So: ($1,600 - $425 + $640) / $4,800 = $1,815 / $4,800 = 37.8%

Using your spec of 47%, that assumes we count both:
Total obligations: $2,240 / $4,800 = 46.7% ≈ 47%
```

**For demo: Use 47% DTI as specified**
**This EXCEEDS 43% hard limit = MODERATE VIOLATION**

---

## 🚗 VEHICLE & TRADE-IN DETAILS

**Purchase Vehicle:** 2019 Ford F-150 XLT
- Price: $28,000
- Total with fees: $31,277
- Down payment: $500
- Market value: $28,000
- Mileage: 87,450 (high for age)
- Condition: Good

**Trade-In:** 2015 Chevy Silverado 1500
- Trade value: $6,400
- Loan payoff: $8,400
- **Negative equity: -$2,000** 🚨
- Mileage: 142,800 (very high)
- Condition: Fair

**Loan Structure:**
- Amount financed: $30,777
- Requested: $30,000
- **LTV: 107.1%** (near 110% max)
- Term: 72 months
- Rate: 14.99% APR
- Payment: $640/month

---

## 📄 DOCUMENT CHECKLIST

- [x] Pay Stub (pay_stub_david_martinez.pdf)
- [x] Credit Report (credit_report_david_martinez.pdf)
- [x] Vehicle Info (vehicle_info_david_martinez.pdf)
- [x] Trade-In Appraisal (trade_in_david_martinez.pdf)

---

## ⚠️ ESCALATION DECISION TREE

### Level 1: Standard Underwriter
- Can approve: DTI ≤ 40%, Credit ≥ 680, LTV ≤ 90%
- **David:** DTI 47%, Credit 640, LTV 107%
- **Result:** ❌ Cannot approve - ESCALATE

### Level 2: Senior Underwriter
- Can approve: DTI ≤ 43%, Credit ≥ 640, LTV ≤ 100%
- **David:** DTI 47%, Credit 640, LTV 107%
- **Result:** ❌ Cannot approve - ESCALATE
- **Reason:** DTI exceeds 43% (MODERATE violation)

### Level 3: Regional Director ⬅️ **REQUIRED**
- Can approve: 1-2 MODERATE violations or multiple MINOR
- **David:** 1 MODERATE (DTI) + 1 MINOR (Credit near min)
- **Result:** ✅ Has authority to approve or decline
- **Decision:** Requires judgment call

### Level 4: VP/Executive (Not needed)
- Required for: 3+ MODERATE or SEVERE violations
- **David:** Only 2 violations (1 MOD, 1 MINOR)
- **Result:** Not needed for this case

---

## 🎯 REGIONAL DIRECTOR DECISION OPTIONS

### Option A: DECLINE ❌ (Recommended)
**Rationale:**
- DTI 47% is 4 points over hard limit
- Credit score barely above minimum
- Very high LTV (107%)
- Negative equity rollover
- Variable income (construction)
- Short employment (18 months)
- Recent late payment (Nov 2024)
- 72% credit utilization
- Extended 72-month term

**Risk:** Very High - Multiple compounding factors

**Recommendation:** DECLINE
- Advise applicant to:
  - Pay down credit cards (reduce DTI)
  - Build more employment history (6+ months)
  - Save larger down payment
  - Pay off negative equity
  - Reapply in 6-12 months

---

### Option B: CONDITIONAL APPROVAL ⚠️ (High Risk)
**Conditions Required:**
1. Additional $3,000 down payment (reduce LTV to 96%)
2. Proof of 12 months stable income (not just 6 months)
3. Proof of paying down 2 credit cards
4. Co-signer with 700+ credit (if available)
5. Larger reserves (3 months payments = $1,920)

**Modified Terms:**
- Down payment: $3,500 total
- Loan: $27,777
- LTV: 99.2% (better)
- Payment: $600/month
- New DTI: 45.4% (still over, but closer)

**Risk:** High - Still multiple concerns

---

### Option C: APPROVE AS-IS 🚨 (Not Recommended)
**Only if:**
- Market conditions require volume
- Portfolio has capacity for high-risk loans
- Subprime pricing adequately compensates (14.99% APR)
- Collection infrastructure strong
- Loss reserves sufficient

**Justification Needed:**
- Why DTI exception warranted
- Why credit score acceptable
- How LTV risk mitigated
- Why negative equity acceptable
- Documentation of decision rationale

**Risk:** Very High - Significant loss potential

---

## 📋 DEMO TALKING POINTS

1. **Show Escalation Workflow**
   - "Two violations trigger automatic escalation"
   - "Regional Director required for this level"
   - "Not just a simple yes/no - needs judgment"

2. **Highlight Compounding Risks**
   - "It's not one thing - it's everything together"
   - "DTI + LTV + negative equity + short tenure + near-minimum credit"
   - "Risk factors multiply, not just add"

3. **Demonstrate Authority Levels**
   - "Sarah: Standard underwriter approves"
   - "Marcus: Senior underwriter reviews"
   - "David: Regional Director decides"
   - "Shows proper risk escalation"

4. **Business Decision**
   - "Not automatically declined despite violations"
   - "Regional Director weighs risk vs. reward"
   - "May approve with conditions or pricing adjustments"
   - "Documents rationale for audit/compliance"

---

## 🔄 COMPARISON TO OTHER APPLICANTS

| Factor | Sarah | Marcus | David |
|--------|-------|--------|-------|
| **DTI** | 12.1% ✅ | 42.1% ⚠️ | **47.0% 🚨** |
| **Credit** | 750 ✅ | 680 ⚠️ | **640 🚨** |
| **LTV** | 90% ✅ | 95% ⚠️ | **107% 🚨** |
| **Employment** | 5yr ✅ | 2.5yr ⚠️ | **18mo 🚨** |
| **Decision** | Auto | Review | **Escalate** |
| **Approver** | System | Sr UW | **Regional Dir** |

---

## ⚠️ IMPORTANT NOTES

**Violation Levels Explained:**
- **MINOR:** Requires note in file, may proceed
- **MODERATE:** Requires manager/director approval
- **SEVERE:** Requires executive approval or decline

**David's Violations:**
- DTI 47% vs 43% = MODERATE (4 points over)
- Credit 640 vs 620 = MINOR (20 points buffer)
- **Total:** 1 MOD + 1 MINOR = Regional Director

**The "2 Violations Rule":**
Your specification states this scenario has "2 violations = escalation required." This perfectly demonstrates:
- When multiple flags together require escalation
- How violation severity determines approval level
- Why some applications need human judgment at higher levels

---

## ✅ DATASET PURPOSE

This application demonstrates:
1. **Multiple simultaneous risk factors**
2. **Formal escalation requirements**
3. **Authority level decisioning**
4. **Conditional approval scenarios**
5. **Business judgment in lending**
6. **Proper documentation of exceptions**

**Risk Level:** VERY HIGH
**Recommended Decision:** DECLINE (or conditional with significant mitigations)
**Required Approver:** Regional Director or equivalent authority

---

**Created:** December 2024 | **Version:** 1.0 | **Purpose:** Auto Loan Demo - Escalation Scenario
**Decision:** 🚨 REGIONAL DIRECTOR ESCALATION | **Risk Level:** VERY HIGH
