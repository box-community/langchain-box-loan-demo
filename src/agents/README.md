# Loan Underwriting Orchestrator Agent

This directory contains the main orchestrator agent for the auto loan underwriting system, built using LangChain's Deep Agents framework.

## Overview

The **LoanUnderwritingOrchestrator** is a sophisticated AI agent that coordinates the complete loan underwriting workflow with:

- **Persistent Memory**: Filesystem-based memory that persists across sessions
- **Planning Capabilities**: Built-in task decomposition and planning tools
- **Violation Framework**: Implements the complete risk-based decisioning system
- **Box Integration**: (To be implemented) Document retrieval and processing
- **Audit Trail**: Complete documentation of all decisions

## Architecture

### Deep Agent Components

The orchestrator uses LangChain's Deep Agents framework with three core middleware:

1. **TodoListMiddleware**: Task planning and tracking
2. **FilesystemMiddleware**: Short-term and long-term memory management
3. **SubAgentMiddleware**: (Future) Delegation to specialized sub-agents

### Memory Architecture

The agent uses a **CompositeBackend** for hybrid memory storage:

```
~/.langchain-box-loan-demo/memories/
├── policies/              # Persistent policy documents
│   ├── underwriting_standards.md
│   ├── approval_authority.md
│   └── valuation_guidelines.md
└── decisions/            # Persistent decision records
    ├── sarah_chen.md
    ├── marcus_johnson.md
    ├── david_martinez.md
    └── jennifer_lopez.md
```

**Memory Routing:**
- `/memories/*` → `FilesystemBackend` (persistent across sessions)
- Other paths → `StateBackend` (ephemeral, per-thread)

### Workflow

```
┌─────────────────────────────────────────────────────┐
│         Loan Application Input                      │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  1. Load Policies from /memories/policies/         │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  2. Retrieve Documents from Box                     │
│     - Pay stubs, tax returns                        │
│     - Credit report, vehicle info                   │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  3. Extract & Validate Data                         │
│     - Income, employment, credit                    │
│     - Vehicle value, loan terms                     │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  4. Calculate Risk Metrics                          │
│     - DTI = (existing + new debt) / income         │
│     - LTV = loan amount / vehicle value            │
│     - Credit score assessment                       │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  5. Identify Violations                             │
│     - MINOR: DTI 43-45%, credit 610-619            │
│     - MODERATE: DTI 45-48%, credit 600-609         │
│     - MAJOR: DTI >48%, credit <600, repo           │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  6. Route Decision                                  │
│     0 violations    → Auto-Approve                  │
│     1-2 minor       → Human Review                  │
│     Moderate/multi  → Escalation                    │
│     Major/3+        → Auto-Deny                     │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  7. Save Decision to /memories/decisions/          │
└─────────────────────────────────────────────────────┘
```

## Usage

### Basic Usage

```python
from agents.orchestrator import create_orchestrator

# Create the orchestrator
orchestrator = create_orchestrator()

# Initialize policies (first run only)
orchestrator.initialize_policies()

# Process a loan application
result = orchestrator.process_loan_application("Sarah Chen")
```

### Advanced Usage

```python
from pathlib import Path
from agents.orchestrator import LoanUnderwritingOrchestrator

# Custom configuration
orchestrator = LoanUnderwritingOrchestrator(
    model="claude-sonnet-4-5-20250929",
    memory_dir=Path("/custom/memory/path"),
    api_key="your-anthropic-api-key"
)

# Check memory status
status = orchestrator.get_memory_status()
print(f"Policies: {len(status['policies']['files'])}")
print(f"Past decisions: {len(status['decisions']['files'])}")

# Process with specific thread ID for conversation continuity
result = orchestrator.process_loan_application(
    applicant_name="Marcus Johnson",
    thread_id="loan_marcus_johnson_20250101"
)
```

## Decision Framework

### Violation Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| **Minor** | Single threshold breach within tolerance | DTI 43-45%, credit 610-619, employment 18-24mo |
| **Moderate** | Larger breach or multiple minor | DTI 45-48%, credit 600-609, LTV >110% |
| **Major** | Severe breach or disqualifying factors | DTI >48%, credit <600, recent repo, 3+ collections |

### Decision Matrix

| Violations | Decision | Approver | SLA |
|------------|----------|----------|-----|
| **0** | Auto-Approve | System | <5 seconds |
| **1-2 Minor** | Human Review | Senior Underwriter | 1-3 days |
| **Moderate or 2+** | Escalation | Regional Director | 3-7 days |
| **Major or 3+** | Auto-Deny | System | <5 seconds |

### Key Thresholds

- **DTI**: 43% maximum (warning at 40%)
- **Credit Score**: 620 minimum
- **Employment**: 2 years minimum
- **Collections**: $5,000 maximum
- **Repossession**: None in 36 months
- **LTV**: 90-120% based on vehicle age

## Configuration

### Environment Variables

Add to your `.env` file:

```bash
# Required for agent operation
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Memory location (optional, defaults to ~/.langchain-box-loan-demo/memories)
AGENT_MEMORY_DIR=/path/to/memory

# Model selection (optional, defaults to claude-sonnet-4-5-20250929)
AGENT_MODEL=claude-sonnet-4-5-20250929
```

## System Prompt

The orchestrator includes a comprehensive system prompt that defines:

1. Core responsibilities (document processing, risk assessment, decision routing)
2. Violation framework and severity levels
3. Key underwriting metrics and thresholds
4. Complete workflow steps
5. Memory management guidelines
6. Audit and compliance requirements

The prompt ensures consistent, conservative risk assessment with complete documentation.

## Best Practices

### Memory Management

1. **Policies** (`/memories/policies/`):
   - Load once during initialization
   - Update when policy changes occur
   - Keep summaries concise for quick reference

2. **Decisions** (`/memories/decisions/`):
   - One file per applicant
   - Include complete violation analysis
   - Document compensating factors
   - Maintain audit trail

3. **Working Files** (ephemeral):
   - Use for temporary calculations
   - Store intermediate analysis
   - Auto-cleaned between threads

### Error Handling

```python
try:
    result = orchestrator.process_loan_application("John Doe")
except Exception as e:
    logger.error(f"Application processing failed: {e}")
    # Handle error appropriately
```

### Thread Management

Use descriptive thread IDs for conversation continuity:

```python
thread_id = f"loan_{applicant_name}_{date}_{sequence}"
result = orchestrator.process_loan_application(
    applicant_name=applicant_name,
    thread_id=thread_id
)
```

## Future Enhancements

### Planned Features

1. **Box API Integration**:
   - Document retrieval tools
   - OCR/text extraction
   - Metadata management

2. **Sub-Agent System**:
   - Specialized credit analysis agent
   - Income verification agent
   - Vehicle valuation agent

3. **Enhanced Memory**:
   - LangGraph Store backend for distributed systems
   - Cross-session learning
   - Pattern recognition across applications

4. **Monitoring & Observability**:
   - LangSmith integration
   - Decision metrics tracking
   - Performance monitoring

## Testing

### Unit Tests

```bash
pytest tests/test_orchestrator.py -v
```

### Integration Tests

```bash
pytest tests/integration/test_loan_workflow.py -v
```

### Sample Applications

Test with the four complete sample applications:

```python
# Auto-approve case
orchestrator.process_loan_application("Sarah Chen")

# Human review case
orchestrator.process_loan_application("Marcus Johnson")

# Escalation case
orchestrator.process_loan_application("David Martinez")

# Auto-deny case
orchestrator.process_loan_application("Jennifer Lopez")
```

## Troubleshooting

### Common Issues

1. **Memory Directory Not Found**:
   ```python
   # Explicitly create memory directory
   memory_dir = Path.home() / ".langchain-box-loan-demo" / "memories"
   memory_dir.mkdir(parents=True, exist_ok=True)
   ```

2. **API Key Not Set**:
   ```bash
   export ANTHROPIC_API_KEY=your_key_here
   ```

3. **Policy Initialization Fails**:
   ```python
   # Manually check policy files exist
   assert Path("data/Policies/Auto Loan Underwriting Standards.md").exists()
   ```

## References

- [LangChain Deep Agents Documentation](https://docs.langchain.com/oss/python/deepagents/overview)
- [LangGraph Documentation](https://docs.langchain.com/langgraph)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- Project CLAUDE.md for domain-specific guidelines
