# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a demonstration project showcasing LangChain's **Deep Agents framework** integrated with **Box AI** via the `box-ai-agents-toolkit` for automated auto loan underwriting. The project demonstrates intelligent, risk-based decision-making using a multi-agent orchestrator pattern that processes sample loan applications across a complete decision spectrum:

- **Auto-Approve** ✅ (Sarah Chen): Perfect borrower profile - zero violations
- **Human Review** ⚠️ (Marcus Johnson): Borderline case requiring senior underwriter review
- **Escalation Required** 🚨 (David Martinez): High-risk case requiring regional director approval
- **Auto-Deny** 🚫 (Jennifer Lopez): Unacceptable risk profile with major violations

The project includes a fully functional research agent as a reference implementation, demonstrating how to build Deep Agents for web research tasks.

## Development Commands

### Environment Setup

This project uses **UV** for dependency management and requires **Python 3.13+**.

```bash
# Install UV package manager if not already installed
# See: https://docs.astral.sh/uv/

# Install dependencies (creates .venv automatically)
uv sync

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Running the Applications

```bash
# Demo 1: Loan Underwriting Agent
python src/demo_loan.py
# Or with UV: uv run src/demo_loan.py

# Demo 2: Research Agent (reference implementation)
python src/demo_research.py
# Or with UV: uv run src/demo_research.py

# Utility: Upload sample loan data to Box
python src/demo_upload_sample_data.py
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

```
langchain-box-loan-demo/
├── src/                          # Main application source code
│   ├── agents/                   # Deep Agents implementations
│   │   ├── loan_underwriting/   # Loan agent module
│   │   │   ├── __init__.py      # Exports for loan agent components
│   │   │   ├── loan_prompts.py  # System prompts for orchestrator & sub-agents
│   │   │   └── loan_tools.py    # LangChain tool wrappers for Box AI
│   │   ├── research_agent/      # Research agent module (reference)
│   │   │   ├── __init__.py
│   │   │   ├── research_prompts.py
│   │   │   └── research_tools.py
│   │   ├── loan_orchestrator.py      # Loan orchestrator factory
│   │   └── orchestrator_research.py  # Research orchestrator factory
│   ├── utils/                   # Shared utilities
│   │   ├── box_api_auth.py      # Box CCG authentication
│   │   ├── box_api_generic.py   # Box API helper functions
│   │   ├── display_messages.py  # Agent message streaming utilities
│   │   └── logging_config.py    # Centralized logging configuration
│   ├── app_config.py            # Application configuration (Pydantic settings)
│   ├── demo_loan.py             # Loan orchestrator demo script
│   ├── demo_research.py         # Research agent demo script
│   └── demo_upload_sample_data.py  # Box data upload utility
│
├── data/                        # Sample loan application data (local copies)
│   ├── Applications/            # Four complete loan applications
│   │   ├── Sarah Chen/          # Folder with applicant documents (PDFs)
│   │   ├── Marcus Johnson/
│   │   ├── David Martinez/
│   │   ├── Jennifer Lopez/
│   │   ├── QUICK_REFERENCE_*.md # Quick reference for each applicant
│   │   └── ULTIMATE_SUMMARY.md  # Complete dataset overview
│   └── Policies/                # Underwriting policy documents (markdown)
│       ├── Auto Loan Underwriting Standards.md
│       ├── Exception Approval Authority.md
│       └── Vehicle Valuation Guidelines.md
│
├── agents_memories/             # Agent persistent memory (FilesystemBackend)
│   ├── box_upload_cache.json   # Box upload tracking (folder/file IDs)
│   └── [Applicant Name]/       # Per-applicant memory folders
│       ├── [Applicant]_data_extraction.md
│       ├── [Applicant]_policy.md
│       ├── [Applicant]_risk_calculation.md
│       ├── [Applicant]_underwriting_decision.md
│       └── [Applicant]_underwriting.md
│
├── .venv/                       # Virtual environment (created by uv sync)
├── pyproject.toml               # UV project configuration & dependencies
├── .env                         # Environment variables (Box & API keys)
├── README.md                    # Project README
└── CLAUDE.md                    # This file (project guidance for Claude)
```

### Key Components

#### Configuration (`src/app_config.py`)

Centralized application configuration using **Pydantic Settings**:
- **Box API credentials**: CCG authentication (client ID, secret, subject)
- **Box folder configuration**: `BOX_DEMO_PARENT_FOLDER`, `BOX_DEMO_FOLDER_NAME`
- **API keys**: `ANTHROPIC_API_KEY`, `TAVILY_API_KEY`
- **Logging**: `LOG_LEVEL`, `LOG_FILE`
- **Agents memory folder**: `AGENTS_MEMORY_FOLDER` (default: `agents_memories`)

The config module initializes:
1. Box client (`conf.box_client`) using CCG auth
2. Local agents memory path (`conf.local_agents_memory`)
3. Logging configuration (via `utils.logging_config`)

**Usage:**
```python
from app_config import conf

# Access Box client
client = conf.box_client

# Access memories folder
memories = conf.local_agents_memory
```

#### Demo Scripts

**`src/demo_loan.py`**: Demonstrates the loan underwriting orchestrator
- Processes loan applications by applicant name
- Uses `loan_orchestrator_create(applicant_name)` factory
- Streams agent responses using `utils.display_messages.stream_agent()`
- Tests one applicant at a time (configurable in `main()`)

**`src/demo_research.py`**: Demonstrates the research agent orchestrator
- Performs web research using Tavily search
- Uses `orchestrator_research.orchestrator_create()` factory
- Reference implementation for building Deep Agents

**`src/demo_upload_sample_data.py`**: Uploads local sample data to Box
- Uploads `data/` folder contents to Box
- Creates folder structure matching local hierarchy
- Saves upload cache to `agents_memories/box_upload_cache.json`
- Required before running loan orchestrator demos

### Domain Model

The loan underwriting system uses a **violation-based decisioning framework**:

#### Key Risk Metrics

1. **DTI (Debt-to-Income) Ratio**: Primary risk indicator
   - Formula: `(existing_monthly_debts + proposed_monthly_payment) / gross_monthly_income`
   - **≤40%**: Normal processing (no violation)
   - **40-43%**: Warning threshold (borderline)
   - **>43%**: Violation (requires exception approval)

2. **Credit Score**: Creditworthiness indicator
   - **≥700**: Excellent (no violation)
   - **660-699**: Good (minor concern)
   - **620-659**: Fair (moderate violation)
   - **<620**: Major violation (auto-deny threshold)

3. **LTV (Loan-to-Value) Ratio**: Collateral coverage
   - Formula: `loan_amount / vehicle_value`
   - Varies by vehicle age (90-120% max per policy)
   - High LTV = higher risk if repossession occurs

#### Violation Severity Classification

- **Minor Violation**: Single small threshold breach within tolerance
  - Examples: DTI 43-45%, credit 610-619
  - Requires: Senior Underwriter approval

- **Moderate Violation**: Larger breach or combination of minor issues
  - Examples: DTI 45-48%, credit 600-609, high LTV
  - Requires: Regional Director approval

- **Major Violation**: Severe breach indicating unacceptable risk
  - Examples: DTI >48%, credit <600, recent repo/bankruptcy
  - Result: Automatic system denial

#### Decision Outcomes

1. **AUTO-APPROVE** ✅
   - Zero violations, all criteria comfortably met
   - Credit ≥700, DTI ≤40%, stable employment
   - System approval, prime rate pricing

2. **HUMAN REVIEW** ⚠️ (Senior Underwriter)
   - 1-2 minor violations
   - Credit 660-699, DTI 40-43%
   - Compensating factors may apply
   - Manual underwriting review required

3. **ESCALATION REQUIRED** 🚨 (Regional Director)
   - 1+ moderate violations OR 2+ minor violations
   - Credit 620-659, DTI 43-48%
   - High LTV, negative equity, or employment instability
   - Requires executive approval with detailed risk analysis

4. **AUTO-DENY** 🚫
   - 3+ violations of any level OR 1+ major violation
   - Credit <620, DTI >48%
   - Recent repo, bankruptcy, or multiple collections
   - Automatic system denial, no manual review

### Integration Points

#### Box AI Integration (via `box-ai-agents-toolkit`)

The project uses the **`box-ai-agents-toolkit`** package for all Box AI interactions:

**Core Functions Used:**
- `box_locate_folder_by_name()`: Search for folders by name
- `box_folder_items_list()`: List folder contents (files/folders)
- `box_ai_ask_file_multi()`: Ask Box AI questions about multiple files
- `box_ai_extract_structured_enhanced_using_fields()`: Extract structured data with field definitions
- `local_file_upload()`: Upload local files to Box
- `box_folder_create()`: Create folders in Box

**Authentication:**
- Uses Box CCG (Client Credentials Grant) authentication
- Configured via `utils.box_api_auth.get_box_client()`
- Credentials stored in `.env` file

**Tool Wrappers (in `src/agents/loan_underwriting/loan_tools.py`):**
All Box AI functions are wrapped as LangChain tools using the `@tool` decorator:
- `search_loan_folder(applicant_name)`: Locate loan folder by name
- `list_loan_documents(folder_id)`: List documents in folder
- `ask_box_ai_about_loan(folder_id, question)`: Query Box AI
- `extract_structured_loan_data(folder_id, fields_schema)`: Extract structured data
- `upload_text_file_to_box(parent_folder_id, file_name, local_file_path)`: Upload file

**Additional Tools:**
- `calculate(expression)`: Safe mathematical expression evaluator
- `think_tool(reflection)`: Strategic reflection and planning tool

#### LangChain Deep Agents Framework

The project uses **LangChain's Deep Agents framework** (`deepagents` package) for multi-agent orchestration:

**Key Concepts:**
- **Orchestrator Pattern**: Main agent coordinates specialized sub-agents
- **Sub-agent Delegation**: Each sub-agent has isolated context and specialized tools
- **Persistent Memory**: Uses `FilesystemBackend` to store conversation state
- **Tool Integration**: LangChain tools provide structured function calling

**Backend Configuration:**
```python
from deepagents.backends import CompositeBackend, FilesystemBackend, StateBackend

# Filesystem backend for persistent memory
filesystem_backend = FilesystemBackend(
    root_dir=str(memories_folder),
    virtual_mode=True  # Virtual paths map to real filesystem
)

# Composite backend routes
def backend(rt):
    return CompositeBackend(
        default=StateBackend(rt),  # In-memory state
        routes={
            "/memories/": filesystem_backend,  # Persistent files
        },
    )
```

**Agent Creation:**
```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model=model,                    # Claude Sonnet 4.5
    tools=[...],                    # Main agent tools
    system_prompt=INSTRUCTIONS,     # System prompt
    subagents=[...],               # Sub-agent definitions
    backend=backend,               # Memory backend
)
```

### Agent Architecture

#### Loan Underwriting Orchestrator

**File:** [src/agents/loan_orchestrator.py](src/agents/loan_orchestrator.py)

**Factory Function:** `loan_orchestrator_create(applicant_name: str) -> CompiledStateGraph`

**Model:** Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)

**Role:** Coordinates the entire loan processing workflow by delegating to three specialized sub-agents.

**Available Tools:**
- `upload_text_file_to_box()`: Upload decision reports to Box

**Workflow:**
1. **Clean up**: Delete any existing files in `/memories/{applicant_name}/`
2. **Plan**: Create todo list breaking down underwriting process
3. **Document Extraction**: Delegate to `box-extract-agent`
4. **Policy Retrieval**: Delegate to `policy-agent`
5. **Risk Calculation**: Delegate to `risk-calculation-agent`
6. **Make Decision**: Synthesize findings and determine outcome
7. **Write Reports**: Generate comprehensive underwriting reports
8. **Upload to Box**: Upload decision documents to applicant's Box folder

**Memory Persistence:**
- Writes to `/memories/{applicant_name}/` (virtual path)
- Maps to `agents_memories/{applicant_name}/` (real filesystem)
- Reports include:
  - `{applicant_name}_data_extraction.md`: Extracted loan data
  - `{applicant_name}_policy.md`: Policy interpretations
  - `{applicant_name}_risk_calculation.md`: Risk calculations
  - `{applicant_name}_underwriting_decision.md`: Final decision
  - `{applicant_name}_underwriting.md`: Orchestrator reflections

#### Sub-Agent 1: Box Extract Agent

**Name:** `box-extract-agent`

**Role:** Retrieves and extracts data from loan application documents in Box

**Available Tools:**
- `search_loan_folder(applicant_name)`: Locate applicant folder by name
- `list_loan_documents(folder_id)`: List all documents in folder
- `ask_box_ai_about_loan(folder_id, question)`: Query Box AI about documents
- `extract_structured_loan_data(folder_id, fields_schema)`: Extract structured fields
- `think_tool(reflection)`: Reflection and planning

**Tasks:**
1. Check `box_upload_cache.json` in memories folder for Box folder IDs
2. Locate loan application folder in Box by applicant name
3. List all documents in the application folder
4. Use Box AI to extract key data points:
   - Applicant information (name, DOB, address)
   - Income details (monthly gross, employer, tenure)
   - Credit information (score, monthly debts, payment history)
   - Vehicle details (year, make, model, price, type)
   - Loan request (amount, term, down payment)
5. Write extraction report to `/memories/{applicant_name}/{applicant_name}_data_extraction.md`

**Expected Output Schema:**
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
    "monthly_debts": 1200,
    "collections": 0,
    "recent_repo": false
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

**Available Tools:**
- `ask_box_ai_about_loan(folder_id, question)`: Query policy documents in Box
- `think_tool(reflection)`: Reflection and analysis

**Tasks:**
1. Query policy documents to retrieve specific thresholds
2. Interpret approval authority levels
3. Explain policy rules in context of current application
4. Write policy analysis to `/memories/{applicant_name}/{applicant_name}_policy.md`

**Example Queries:**
- "What is the maximum DTI ratio for standard approval?"
  - Expected: "43% per Auto Loan Underwriting Standards"
- "What LTV is allowed for a 3-year-old used vehicle?"
  - Expected: "100% per Vehicle Valuation Guidelines"
- "What approval authority is needed for DTI between 43-45%?"
  - Expected: "Senior Underwriter per Exception Approval Authority"

#### Sub-Agent 3: Risk Calculation Agent

**Name:** `risk-calculation-agent`

**Role:** Performs quantitative risk analysis and violation detection

**Available Tools:**
- `calculate(expression)`: Safe mathematical expression evaluator
- `think_tool(reflection)`: Show calculation work

**Tasks:**
1. Calculate **DTI ratio**: `(monthly_debts + proposed_payment) / monthly_income`
2. Calculate **LTV ratio**: `loan_amount / vehicle_value`
3. Identify policy violations and classify severity (minor/moderate/major)
4. Assess overall risk level based on violation count and type
5. Calculate vehicle depreciation over loan term
6. Write risk analysis to `/memories/{applicant_name}/{applicant_name}_risk_calculation.md`

**Policy Thresholds:**
- **DTI**: ≤40% (normal), 40-43% (warning), >43% (violation)
- **Credit**: ≥700 (excellent), 660-699 (good), 620-659 (fair), <620 (major violation)
- **LTV**: Varies by vehicle age (90-120% max)

**Violation Severity Classification:**
- **Minor**: Single small breach (DTI 43-45%, credit 610-619)
- **Moderate**: Larger breach (DTI 45-48%, credit 600-609)
- **Major**: Severe breach (DTI >48%, credit <600, recent repo)

**Expected Output Schema:**
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

#### Research Agent (Reference Implementation)

**File:** [src/agents/orchestrator_research.py](src/agents/orchestrator_research.py)

**Factory Function:** `orchestrator_create() -> CompiledStateGraph`

**Model:** Claude Sonnet 4.5

**Role:** Demonstrates how to build a Deep Agent for web research tasks using Tavily search.

**Sub-agent:**
- `research-agent`: Delegates research topics to specialized researcher
  - Tools: `tavily_search()`, `think_tool()`

**Usage:** Reference this implementation when building new Deep Agents.

## Sample Data

### Four Complete Loan Applications

Located in `data/Applications/`:

1. **Sarah Chen** ✅ (Auto-Approve)
   - Credit: 750, DTI: 12.1%, LTV: 90%
   - Income: $7,500/mo, stable employment (5 years)
   - Vehicle: 2024 Honda Accord (new), $27K
   - Zero violations, perfect borrower

2. **Marcus Johnson** ⚠️ (Human Review)
   - Credit: 680, DTI: 42.1%, LTV: 95%
   - Income: $5,200/mo, stable employment
   - Vehicle: 2021 Toyota Camry (used), $22K
   - Zero violations, but borderline DTI

3. **David Martinez** 🚨 (Escalation Required)
   - Credit: 640, DTI: 47.0%, LTV: 107%
   - Income: $4,800/mo, employment concerns
   - Vehicle: 2019 Honda Civic (used), $18K
   - 2 violations: 1 moderate (DTI), 1 minor (LTV)

4. **Jennifer Lopez** 🚫 (Auto-Deny)
   - Credit: 575, DTI: 54.7%, LTV: 100%
   - Income: $3,800/mo, unstable employment
   - Vehicle: 2022 Nissan Altima (used), $20K
   - 3+ violations: major credit, major DTI, repo history

### Policy Documents

Located in `data/Policies/`:

1. **Auto Loan Underwriting Standards.md**: Core approval criteria (DTI, credit, LTV)
2. **Exception Approval Authority.md**: Who can approve violations
3. **Vehicle Valuation Guidelines.md**: LTV limits by vehicle age

**Note:** All sample data is **completely fictional** and marked as "DEMO DATA" for testing purposes only.

## Implementation Guidelines

### Using the Loan Orchestrator

```python
import asyncio
from agents.loan_orchestrator import loan_orchestrator_create
from utils.display_messages import stream_agent

async def process_loan(applicant_name: str):
    # Create the orchestrator (pass applicant name)
    agent = loan_orchestrator_create(applicant_name=applicant_name)

    # Process the loan application
    request = f"Please process the auto loan application for {applicant_name}"

    # Stream the response
    await stream_agent(
        agent,
        {"messages": [{"role": "user", "content": request}]},
    )

# Run the orchestrator
asyncio.run(process_loan("Sarah Chen"))
```

### Key Implementation Patterns

1. **Box Integration**: All tools use `conf.box_client` for authentication
   ```python
   from app_config import conf

   # Box client is already initialized
   client = conf.box_client
   ```

2. **Tool Wrappers**: Use LangChain `@tool` decorator for all tools
   ```python
   from langchain_core.tools import tool

   @tool(parse_docstring=True)
   def my_tool(arg: str) -> str:
       """Tool description.

       Args:
           arg: Argument description

       Returns:
           Return value description
       """
       return f"Result: {arg}"
   ```

3. **Memory Persistence**: Write reports to `/memories/` virtual path
   ```python
   # Virtual path (as seen by agent)
   virtual_path = "/memories/applicant/report.md"

   # Real path (filesystem)
   real_path = conf.local_agents_memory / "applicant" / "report.md"
   ```

4. **Sub-agent Delegation**: Use `task()` tool in system prompts
   ```python
   # Orchestrator delegates to sub-agent
   result = task(
       agent="box-extract-agent",
       task="Extract loan data for Sarah Chen"
   )
   ```

5. **Violation Framework**: Always classify violations by severity
   - Count total violations by type (minor, moderate, major)
   - Apply decision framework based on violation counts
   - Document all violations in reports

### Guidelines for Extensions

When extending the system:

1. **Follow the Authority Matrix**: Ensure decisions respect approval authority levels
2. **Calculate DTI Correctly**: `(existing_debt + proposed_payment) / monthly_income`
3. **Apply Violation Rules Strictly**: Track all violations and classify severity
4. **Use Box AI Tools**: Prefer Box AI Ask/Extract over manual parsing
5. **Maintain Audit Trail**: Document all decision factors in reports
6. **Test All Decision Paths**: Verify auto-approve, review, escalation, and deny outcomes
7. **Use UV for Dependencies**: Always use `uv sync` and `uv add` for package management
8. **Configure via .env**: Never hardcode credentials or folder IDs

## Running the System

### Prerequisites

1. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Configure `.env` file** with Box and API credentials:
   ```env
   # Box API Configuration (CCG Auth)
   BOX_CLIENT_ID=your_client_id
   BOX_CLIENT_SECRET=your_client_secret
   BOX_SUBJECT_TYPE=user
   BOX_SUBJECT_ID=your_subject_id
   BOX_DEMO_PARENT_FOLDER=parent_folder_id
   BOX_DEMO_FOLDER_NAME=LangChain Meetup Demo

   # API Keys
   ANTHROPIC_API_KEY=your_anthropic_key
   TAVILY_API_KEY=your_tavily_key

   # Agent Configuration
   AGENTS_MEMORY_FOLDER=agents_memories

   # Logging (optional)
   LOG_LEVEL=INFO
   LOG_FILE=
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   source .venv/bin/activate  # macOS/Linux
   ```

4. **Upload sample data to Box**:
   ```bash
   python src/demo_upload_sample_data.py
   ```

   This creates:
   - Box folder structure matching `data/` directory
   - `agents_memories/box_upload_cache.json` with folder/file IDs

### Running the Loan Orchestrator

```bash
# Test with a single applicant (edit demo_loan.py to select)
python src/demo_loan.py

# Expected outcomes:
# - Sarah Chen: AUTO-APPROVE ✅ (750 credit, 12.1% DTI)
# - Marcus Johnson: HUMAN REVIEW ⚠️ (680 credit, 42.1% DTI)
# - David Martinez: ESCALATION REQUIRED 🚨 (640 credit, 47.0% DTI, 2 violations)
# - Jennifer Lopez: AUTO-DENY 🚫 (575 credit, 54.7% DTI, repo history)
```

### Running the Research Agent

```bash
# Test the research agent (reference implementation)
python src/demo_research.py
```

## Dependencies

### Core Dependencies (in `pyproject.toml`)

- **`box-ai-agents-toolkit` (≥0.1.5)**: Box AI integration toolkit
- **`deepagents` (≥0.3.0)**: LangChain Deep Agents framework
- **`langchain-anthropic` (≥1.2.0)**: Claude model integration
- **`langgraph` (≥1.0.4)**: Graph-based agent orchestration
- **`pydantic` (≥2.12.5)**: Data validation and settings
- **`pydantic-settings` (≥2.12.0)**: Environment-based configuration
- **`python-dotenv` (≥1.2.1)**: `.env` file loading
- **`tavily` (≥1.1.0)**: Web search API (for research agent)
- **`colorlog` (≥6.9.0)**: Colored logging output
- **`rich` (≥14.2.0)**: Rich text and formatting
- **`markdownify` (≥1.2.2)**: HTML to Markdown conversion
- **`ipython` (≥9.8.0)**: Interactive Python shell

### Development Dependencies

- **`pytest` (≥9.0.2)**: Testing framework
- **`pytest-cov` (≥7.0.0)**: Code coverage
- **`ruff` (≥0.14.8)**: Linting and formatting

### Python Version

- **Requires Python 3.13+** (specified in `pyproject.toml`)

## Important Notes

- ✅ **Implementation Status**: Core orchestrator and 3 sub-agents fully implemented
- 📦 **Package Manager**: UV (not pip or poetry)
- 🐍 **Python Version**: 3.13+ required
- 📄 **Demo Data**: All loan applications are completely fictional
- 📦 **Box Setup**: Sample data must be uploaded to Box via `demo_upload_sample_data.py`
- 🔑 **Authentication**: Box CCG (Client Credentials Grant) configured in `.env`
- 💾 **Memory**: Agent state persists in `agents_memories/` folder
- 🤖 **Model**: Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- 🔍 **Search**: Tavily API used for web research (research agent only)

## Troubleshooting

### Common Issues

1. **Box authentication errors**:
   - Verify `.env` credentials are correct
   - Check Box CCG app has proper scopes
   - Ensure `BOX_DEMO_PARENT_FOLDER` exists

2. **"Folder not found" errors**:
   - Run `demo_upload_sample_data.py` first
   - Check `box_upload_cache.json` exists in `agents_memories/`

3. **Module import errors**:
   - Run `uv sync` to install dependencies
   - Activate virtual environment: `source .venv/bin/activate`

4. **Agent memory issues**:
   - Delete `agents_memories/{applicant_name}/` to reset
   - Verify `AGENTS_MEMORY_FOLDER` in `.env`

5. **Python version errors**:
   - Project requires Python 3.13+
   - Use `python --version` to check your version
