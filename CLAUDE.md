# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a demonstration project showcasing LangChain's Deep Agent framework integrated with Box API for automated auto loan underwriting. The project uses sample loan applications to demonstrate intelligent, risk-based decisioning across a complete spectrum:

- **Auto-Approve** (Sarah Chen): Perfect borrower profile
- **Human Review** (Marcus Johnson): Borderline case requiring underwriter review
- **Escalation** (David Martinez): High-risk case requiring director approval
- **Auto-Deny** (Jennifer Lopez): Unacceptable risk profile

## Development Commands

### Environment Setup
```bash
# Install UV package manager if not already installed
# The project uses UV for dependency management

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Running the Application
```bash
# Run the main application
python src/main.py

# Or with UV
uv run src/main.py

# Test the loan underwriting orchestrator
python src/test_loan_orchestrator.py
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest path/to/test_file.py

# Run tests with verbose output
pytest -v

# Run tests with coverage
pytest --cov=src
```

### Code Quality
```bash
# Run linter (Ruff)
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Format code
ruff format .
```

## Architecture

### Directory Structure

- `src/`: Main application source code
  - `agents/`: LangChain Deep Agents for loan processing
    - `loan_underwriting/`: Loan orchestrator implementation
      - `loan_prompts.py`: System prompts for orchestrator and sub-agents
      - `loan_tools.py`: LangChain tool wrappers for Box AI integration
    - `loan_orchestrator.py`: Main orchestrator factory
    - `research_agent/`: Research agent example (for reference)
  - `utils/`: Helper utilities for Box auth and logging
  - `main.py`: Application entry point
  - `test_loan_orchestrator.py`: Test script for loan processing

- `data/`: Sample loan application data
  - `Applications/`: Four complete loan applications with supporting documents
    - Each applicant has PDFs (pay stubs, credit reports, tax returns, etc.)
    - QUICK_REFERENCE files provide summarized metrics
    - ULTIMATE_SUMMARY.md contains complete dataset overview
  - `Policies/`: Underwriting policy documents
    - Auto Loan Underwriting Standards
    - Exception Approval Authority
    - Vehicle Valuation Guidelines

- `docs/`: Project documentation (currently empty)

### Domain Model

The loan underwriting system uses a **violation-based decisioning framework**:

**Key Metrics:**
- **DTI (Debt-to-Income) Ratio**: Primary risk indicator
  - ≤40%: Normal processing
  - 40-43%: Warning threshold
  - \>43%: Violation (requires exception approval)
- **Credit Score**: Minimum 620 required
- **LTV (Loan-to-Value)**: Varies by vehicle age (90-120%)

**Violation Levels:**
- **Minor**: Single threshold breach within tolerance (e.g., DTI 43-45%, credit 610-619)
  - Requires manager approval
- **Moderate**: Larger breach or combination of minor violations (e.g., DTI 45-48%)
  - Requires Regional Director approval
- **Major**: Severe breach or 3+ violations (e.g., DTI >48%, credit <600, recent repo)
  - Automatic denial

**Decision Outcomes:**
1. **Auto-Approve**: Zero violations, all criteria met
2. **Human Review**: 1-2 minor violations, compensating factors may apply
3. **Escalation Required**: Moderate violations or multiple minor violations
4. **Auto-Deny**: Major violations or 3+ violations of any level

### Integration Points

**Box AI Integration** (implemented via `box_ai_agents_toolkit`):
- **Box AI Ask**: Query documents with natural language questions
- **Box AI Extract Structured**: Extract structured data from unstructured documents
- **Box Folder Operations**: Search, list, and organize loan application folders
- All Box operations use the Box SDK with CCG authentication (configured in `.env`)

**LangChain Deep Agents Framework** (implemented):
- **Orchestrator Pattern**: Main agent coordinates specialized sub-agents
- **Sub-agent Delegation**: Each sub-agent has isolated context and specialized tools
- **Persistent Memory**: Uses FilesystemBackend to maintain conversation state
- **Tool Integration**: LangChain tool wrappers around Box AI functionality

### Agent Architecture

**Implementation Status:** ✅ Fully Implemented

The loan underwriting system uses LangChain's Deep Agents framework with an orchestrator pattern coordinating three specialized sub-agents.

#### Main Orchestrator

**File:** `src/agents/loan_orchestrator.py`
**Role:** Coordinates the entire loan processing workflow
**Model:** Claude Sonnet 4.5
**Responsibilities:**

- Receives loan application requests (by applicant name)
- Delegates tasks to specialized sub-agents
- Synthesizes findings from all sub-agents
- Makes final underwriting decision
- Generates comprehensive underwriting reports
- Maintains conversation memory in `/memories/` folder

**Workflow:**
1. Plan the underwriting process (create todo list)
2. Delegate to box-extract-agent for document retrieval
3. Delegate to policy-agent for rule interpretation
4. Delegate to risk-calculation-agent for quantitative analysis
5. Synthesize all findings and make decision
6. Write final report to `/memories/underwriting_decision.md`

#### Sub-Agent 1: Box Extract Agent

**Name:** `box-extract-agent`
**Role:** Retrieves and extracts data from loan application documents in Box
**Tools Available:**
- `search_loan_folder()` - Locate applicant folder by name
- `list_loan_documents()` - List all documents in folder
- `ask_box_ai_about_loan()` - Query Box AI about documents
- `extract_structured_loan_data()` - Extract structured fields using Box AI Extract
- `think_tool()` - Reflection and planning

**Tasks:**
- Locate loan application folder in Box by applicant name
- List all documents in the application folder
- Use Box AI to extract key data points:
  - Applicant information (name, DOB, address)
  - Income details (monthly gross, employer, tenure)
  - Credit information (score, monthly debts, payment history)
  - Vehicle details (year, make, model, price, type)
  - Loan request (amount, term, down payment)

**Output Schema:**

```json
{
  "applicant": {
    "name": "John Doe",
    "dob": "1985-03-15",
    "address": "123 Main St, Austin, TX"
  },
  "income": {
    "monthly_gross": 6500,
    "annual_gross": 78000,
    "employer": "Tech Corp Inc",
    "years_employed": 3.5
  },
  "credit": {
    "score": 720,
    "monthly_debts": 1200
  },
  "vehicle": {
    "year": 2024,
    "make": "Toyota",
    "model": "Camry",
    "purchase_price": 28500,
    "vehicle_type": "new"
  },
  "loan_request": {
    "amount": 25000,
    "term_months": 60,
    "down_payment": 3500
  }
}
```

#### Sub-Agent 2: Policy Agent

**Name:** `policy-agent`
**Role:** Interprets underwriting policies and compliance rules
**Tools Available:**
- `ask_box_ai_about_loan()` - Query policy documents in Box
- `think_tool()` - Reflection and analysis

**Tasks:**
- Query policy documents to retrieve specific thresholds
- Interpret approval authority levels
- Explain policy rules in context of current application

**Example Queries:**
- "What is the maximum DTI ratio for standard approval?"
  → Answer: "43% per Auto Loan Underwriting Standards"
- "What LTV is allowed for a 3-year-old used vehicle?"
  → Answer: "100% per Vehicle Valuation Guidelines"
- "What approval authority is needed for DTI between 43-45%?"
  → Answer: "Senior Underwriter per Exception Approval Authority"

#### Sub-Agent 3: Risk Calculation Agent

**Name:** `risk-calculation-agent`
**Role:** Performs quantitative risk analysis and violation detection
**Tools Available:**
- `calculate()` - Mathematical expression evaluator
- `think_tool()` - Show calculation work

**Tasks:**
- Calculate Debt-to-Income (DTI) ratio: `(monthly_debts + proposed_payment) / monthly_income`
- Calculate Loan-to-Value (LTV) ratio: `loan_amount / vehicle_value`
- Identify policy violations and classify severity (minor/moderate/major)
- Assess overall risk level based on violation count and type
- Calculate vehicle depreciation over loan term

**Policy Thresholds:**
- DTI: ≤40% (normal), 40-43% (warning), >43% (violation)
- Credit: ≥700 (excellent), 660-699 (good), 620-659 (fair), <620 (major violation)
- LTV: Varies by vehicle age (90-120% max)

**Violation Severity:**
- **Minor**: Single small breach (DTI 43-45%, credit 610-619)
- **Moderate**: Larger breach (DTI 45-48%, credit 600-609)
- **Major**: Severe breach (DTI >48%, credit <600, recent repo)

**Output Schema:**

```json
{
  "metrics": {
    "dti": 0.421,
    "ltv": 0.95,
    "credit_score": 680
  },
  "violations": [
    {
      "rule": "DTI Maximum",
      "threshold": 0.43,
      "actual": 0.421,
      "severity": "none"
    }
  ],
  "risk_level": "low|moderate|high|unacceptable",
  "total_violations": 0,
  "violation_breakdown": {
    "minor": 0,
    "moderate": 0,
    "major": 0
  }
}
```

### Decision Framework (Orchestrator's Final Output)

The orchestrator synthesizes all sub-agent findings and produces one of four decisions:

**1. AUTO-APPROVE ✅**
- Zero violations + credit ≥700 + DTI ≤40%
- System approval, prime rate pricing

**2. HUMAN REVIEW (Senior Underwriter) ⚠️**
- 1-2 minor violations
- Credit 660-699, DTI 40-43%
- Compensating factors may apply

**3. ESCALATION REQUIRED (Regional Director) 🚨**
- 1+ moderate violations OR 2+ minor violations
- Credit 620-659, DTI 43-48%
- High LTV or negative equity

**4. AUTO-DENY 🚫**
- 3+ violations OR 1+ major violation
- Credit <620, DTI >48%
- Recent repo/bankruptcy/collections

## Sample Data Structure

Each loan application includes:
- **Pay Stubs**: Monthly income verification
- **Tax Returns**: Annual income verification
- **Credit Reports**: Credit score, payment history, collections
- **Vehicle Information**: Purchase price, valuation, trade-in details
- **Purchase Agreements**: Loan terms, down payment, financing structure

All sample data is completely fictional and clearly marked as "DEMO DATA" for testing purposes only.

## Implementation Guidelines

### Using the Loan Orchestrator

The loan underwriting orchestrator is fully implemented and ready to use:

```python
from agents.loan_orchestrator import loan_orchestrator_create

# Create the orchestrator
agent = loan_orchestrator_create()

# Process a loan application
request = "Please process the auto loan application for Sarah Chen"

# Stream the response
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": request}]},
    stream_mode="messages"
):
    print(chunk)
```

### Key Implementation Patterns

1. **Box Integration**: All tools use `config.box_client` for authentication
2. **Tool Wrappers**: LangChain `@tool` decorator wraps Box AI functions
3. **Memory Persistence**: `/memories/` folder stores conversation state and reports
4. **Sub-agent Delegation**: Use `task()` tool to delegate to specialized sub-agents
5. **Violation Framework**: Risk calculations must classify violations by severity

### Guidelines for Extensions

When extending the system:

1. **Follow the Authority Matrix**: Ensure decisions respect approval authority levels
2. **Calculate DTI Correctly**: `(existing_debt + proposed_payment) / monthly_income`
3. **Apply Violation Rules Strictly**: Track all violations and classify severity
4. **Use Box AI Tools**: Prefer Box AI Ask/Extract over manual parsing
5. **Maintain Audit Trail**: Document all decision factors in reports
6. **Test All Decision Paths**: Verify auto-approve, review, escalation, and deny outcomes

## Important Notes

- **Implementation Status**: Core orchestrator and 3 sub-agents fully implemented ✅
- **Python Version**: 3.11+ required (project tested with 3.11)
- **Package Manager**: UV (not pip or poetry)
- **Demo Data**: All loan applications are fictional for demonstration only
- **Box Setup Required**: Loan applications must be uploaded to Box and `BOX_DEMO_PARENT_FOLDER` configured
- **Dependencies**:
  - `box_ai_agents_toolkit` - Box AI integration
  - `deepagents` - LangChain Deep Agents framework
  - `langchain-anthropic` - Claude model integration

## Running the Orchestrator

### Prerequisites

1. Upload sample loan applications to Box (or use existing Box folders)
2. Configure `.env` file with Box credentials:
   ```
   BOX_CLIENT_ID=your_client_id
   BOX_CLIENT_SECRET=your_client_secret
   BOX_SUBJECT_TYPE=user
   BOX_SUBJECT_ID=your_subject_id
   BOX_DEMO_PARENT_FOLDER=parent_folder_id
   ANTHROPIC_API_KEY=your_api_key
   ```

### Test the System

```bash
# Test with a single applicant
python src/test_loan_orchestrator.py

# Or import and use in your own code
from agents.loan_orchestrator import loan_orchestrator_create
agent = loan_orchestrator_create()
```

### Expected Test Results

- **Sarah Chen**: AUTO-APPROVE ✅ (750 credit, 12.1% DTI)
- **Marcus Johnson**: HUMAN REVIEW ⚠️ (680 credit, 42.1% DTI)
- **David Martinez**: ESCALATION REQUIRED 🚨 (640 credit, 47.0% DTI, 2 violations)
- **Jennifer Lopez**: AUTO-DENY 🚫 (575 credit, 54.7% DTI, repo history)
