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
  - `agents/`: LangChain agents for loan processing (empty, to be implemented)
  - `tools/`: Custom tools for Box API integration and document processing (empty, to be implemented)
  - `utils/`: Helper utilities (empty, to be implemented)
  - `main.py`: Application entry point

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

**Box API** (to be implemented):
- Document storage and retrieval
- OCR/text extraction from application documents
- Metadata management for loan applications

**LangChain Framework** (to be implemented):
- Agent orchestration for multi-step underwriting workflow
- Tool integration for Box API calls
- Document analysis and data extraction
- Decision reasoning and explanation

## Sample Data Structure

Each loan application includes:
- **Pay Stubs**: Monthly income verification
- **Tax Returns**: Annual income verification
- **Credit Reports**: Credit score, payment history, collections
- **Vehicle Information**: Purchase price, valuation, trade-in details
- **Purchase Agreements**: Loan terms, down payment, financing structure

All sample data is completely fictional and clearly marked as "DEMO DATA" for testing purposes only.

## Implementation Guidelines

When building agents and tools:

1. **Follow the Authority Matrix**: Ensure decisions respect the exception approval authority levels defined in policies
2. **Calculate DTI Correctly**: Total monthly debt (existing + proposed) / gross monthly income
3. **Apply Violation Rules Strictly**: Track all violations and their severity levels
4. **Consider Compensating Factors**: Large down payments, reserves, or co-signers may offset violations
5. **Maintain Audit Trail**: Document all decision factors and approval authority
6. **Use Policy Documents**: Reference the markdown files in `data/Policies/` for underwriting rules

## Important Notes

- This project is in early development (v0.1.0)
- Python 3.13+ is required
- The project uses UV for package management (not pip or poetry)
- All loan application data is fictional and for demonstration purposes only
