# LangChain Deep Agents Framework

## Overview

**Deep Agents** is a LangChain framework for building sophisticated multi-agent systems using an orchestrator pattern. It provides a structured approach to creating intelligent agent architectures where a main orchestrator coordinates specialized sub-agents, each with isolated contexts and focused responsibilities.

### Core Philosophy

- **Agents have focused, specialized roles** - Each agent excels at a specific type of task
- **Orchestrators coordinate and synthesize** - Main agent manages workflow and combines findings
- **Isolated contexts and memory** - Each agent maintains its own state and tool access
- **Tools as the primary interface** - Agents interact with systems through structured function calling

**Framework Package:** `deepagents` (≥0.3.0)

---

## Key Concepts

### 1. Orchestrators vs Sub-Agents

#### Orchestrators

The main agent that coordinates the overall workflow:

- **Higher-level decision-making** - Plans strategy and manages execution flow
- **Synthesis of findings** - Combines results from multiple sub-agents
- **Workflow coordination** - Delegates tasks and orchestrates sequence
- **Focused tool access** - Only tools needed for coordination (not domain-specific tools)

**Example:** The loan underwriting orchestrator manages the entire loan processing workflow

#### Sub-Agents

Specialized agents with narrow, focused responsibilities:

- **Domain expertise** - Deep knowledge in a specific area
- **Isolated execution contexts** - Cannot see orchestrator's full state
- **Limited tool access** - Only tools relevant to their specialty
- **Cannot invoke other sub-agents** - Must return findings to orchestrator
- **Stateless delegation** - Each invocation is independent

**Example Sub-Agents in This Project:**
```
├── box-extract-agent - Document extraction from Box
├── policy-agent - Policy interpretation and compliance
└── risk-calculation-agent - Quantitative risk analysis
```

### 2. Backends & Memory Management

Deep Agents supports multiple backend types for state and memory persistence:

#### StateBackend - In-Memory State

```python
StateBackend(rt)
```

- **Ephemeral storage** - Data exists only during agent execution
- **Fast access** - No I/O overhead
- **Use case** - Temporary conversation state, intermediate calculations

#### FilesystemBackend - Persistent File Storage

```python
FilesystemBackend(
    root_dir=str(memories_folder),
    virtual_mode=True,
)
```

- **Persistent storage** - Data survives agent restarts
- **Virtual path mapping** - Agents use logical paths (e.g., `/memories/`) that map to real filesystem
- **Audit trail** - Creates permanent records of agent decisions
- **Use case** - Decision reports, extracted data, compliance documentation

**Virtual Mode Example:**
```python
# Agent writes to virtual path
Agent: "Write to /memories/applicant/report.md"

# Actually persists to physical path
Filesystem: "agents_memories/applicant/report.md"
```

#### CompositeBackend - Hybrid Storage Routing

```python
CompositeBackend(
    default=StateBackend(rt),              # General ephemeral state
    routes={
        "/memories/": filesystem_backend,  # Persistent files
    },
)
```

- **Route-based delegation** - Different paths go to different backends
- **Flexible strategies** - Mix ephemeral and persistent storage
- **Use case** - Store conversation state in memory, decision reports on disk

**This Project's Memory Structure:**
```
agents_memories/
├── box_upload_cache.json              # Box folder ID cache
└── {applicant_name}/                  # Per-applicant memory
    ├── {applicant}_data_extraction.md
    ├── {applicant}_policy.md
    ├── {applicant}_risk_calculation.md
    ├── {applicant}_underwriting_decision.md
    └── {applicant}_underwriting.md
```

### 3. Tool Integration with LangChain

Deep Agents integrates seamlessly with LangChain's tool system:

#### Tool Definition Pattern

```python
from langchain_core.tools import tool

@tool(parse_docstring=True)
def search_loan_folder(applicant_name: str) -> str:
    """Locate loan application folder by applicant name.

    Args:
        applicant_name: Full name of the loan applicant

    Returns:
        Box folder ID containing applicant's documents
    """
    # Implementation here
    return folder_id
```

**Key Features:**
- `@tool` decorator converts functions to LangChain tools
- `parse_docstring=True` extracts descriptions from docstring
- Type hints provide automatic validation
- Docstring appears in agent's tool instructions

#### Tool Categories in This Project

**1. Query Tools** - Ask questions about data
```python
ask_box_ai_about_loan(folder_id, question)
```

**2. List Tools** - Retrieve structured data
```python
list_loan_documents(folder_id)
```

**3. Search Tools** - Find information
```python
search_loan_folder(applicant_name)
```

**4. Calculate Tools** - Perform computations
```python
calculate(expression)  # Safe math eval
```

**5. Write Tools** - Persist data
```python
upload_text_file_to_box(parent_folder_id, file_name, local_file_path)
```

**6. Reflection Tools** - Strategic thinking
```python
think_tool(reflection)  # Deliberate pause for analysis
```

---

## Creating Deep Agents

### Factory Function Pattern

Deep Agents are created using a factory function pattern:

```python
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, FilesystemBackend, StateBackend
from langchain.chat_models import init_chat_model

def agent_orchestrator_create(applicant_name: str) -> CompiledStateGraph:
    """Create a deep agent orchestrator for loan underwriting."""

    # 1. Initialize the LLM model
    model = init_chat_model(
        model="anthropic:claude-sonnet-4-5-20250929",
        temperature=0.0,  # Deterministic decisions
        api_key=conf.ANTHROPIC_API_KEY,
    )

    # 2. Define sub-agents
    sub_agents = [
        {
            "name": "box-extract-agent",
            "description": "Extracts loan data from Box documents",
            "system_prompt": BOX_EXTRACT_INSTRUCTIONS,
            "tools": [search_loan_folder, list_documents, ask_box_ai, think_tool],
        },
        {
            "name": "policy-agent",
            "description": "Interprets underwriting policies",
            "system_prompt": POLICY_INSTRUCTIONS,
            "tools": [ask_box_ai, think_tool],
        },
        {
            "name": "risk-calculation-agent",
            "description": "Calculates risk metrics and violations",
            "system_prompt": RISK_CALCULATION_INSTRUCTIONS,
            "tools": [calculate, think_tool],
        },
    ]

    # 3. Configure persistent memory
    memories_folder = conf.local_agents_memory / applicant_name
    filesystem_backend = FilesystemBackend(
        root_dir=str(memories_folder),
        virtual_mode=True,
    )

    def backend(rt):
        return CompositeBackend(
            default=StateBackend(rt),
            routes={
                "/memories/": filesystem_backend,
            },
        )

    # 4. Create the orchestrator agent
    agent = create_deep_agent(
        model=model,
        tools=[upload_text_file_to_box],
        system_prompt=ORCHESTRATOR_INSTRUCTIONS,
        subagents=sub_agents,
        backend=backend,
    )

    return agent
```

### Parameters of `create_deep_agent()`

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | LLM instance | Chat model (Claude, GPT, Gemini, etc.) |
| `tools` | List[Tool] | Tools available to the orchestrator |
| `system_prompt` | str | Instructions for the orchestrator |
| `subagents` | List[Dict] | Sub-agent definitions (name, description, prompt, tools) |
| `backend` | Callable | Factory function returning a backend instance |

**Return Type:** `CompiledStateGraph` - A LangGraph state machine ready for execution

### Sub-Agent Definition Structure

Each sub-agent requires:

```python
{
    "name": "agent-identifier",           # Unique ID for delegation
    "description": "Brief role summary",   # When to use this agent
    "system_prompt": "Detailed instructions...",
    "tools": [tool1, tool2, tool3],       # Tools specific to this agent
}
```

---

## Sub-Agent Delegation

### How Delegation Works

The orchestrator delegates tasks through instructions in its system prompt:

```python
ORCHESTRATOR_INSTRUCTIONS = """
You orchestrate the loan underwriting workflow by delegating to specialists.

## Delegation Strategy

1. **box-extract-agent** - Extracts all loan application data from Box
2. **policy-agent** - Retrieves underwriting policy thresholds
3. **risk-calculation-agent** - Calculates DTI, LTV, and identifies violations

## Workflow

1. Delegate to box-extract-agent: "Extract loan data for {applicant_name}"
2. Delegate to policy-agent: "Retrieve DTI and credit score thresholds"
3. Delegate to risk-calculation-agent: "Calculate risk metrics and violations"
4. Synthesize findings and make underwriting decision
"""
```

### Delegation Best Practices

**1. Start with one sub-agent** for single-aspect tasks
```python
# Good: Focused delegation
"Delegate to box-extract-agent: Extract all loan data for Sarah Chen"

# Avoid: Splitting unnecessarily
"Delegate to agent A: Get name"
"Delegate to agent B: Get income"
```

**2. Parallelize for independent tasks**
```python
# When tasks don't depend on each other
"Delegate to research-agent-1: Research topic A"
"Delegate to research-agent-2: Research topic B"
# Wait for both, then synthesize
```

**3. Sequential for dependent tasks**
```python
# When output of one feeds into another
"Delegate to extract-agent: Get loan data"
# Wait for result
"Delegate to risk-agent: Calculate DTI using extracted data"
```

**4. Limit concurrency**
- Typically max 2-3 parallel sub-agents per iteration
- More parallelism = more cost and complexity
- Prefer sequential for clarity

---

## Memory Management

### Writing to Memory

Agents write to memory using virtual paths:

```python
# In sub-agent system prompt
"""
After extraction, write your findings to:
/memories/{applicant_name}/{applicant_name}_data_extraction.md

Include:
- Applicant information
- Income details
- Credit information
- Vehicle details
- Loan request
"""
```

### Reading from Memory

Agents can reference previously written memories:

```python
# In orchestrator system prompt
"""
Review the following memory files:
- /memories/{applicant_name}/{applicant_name}_data_extraction.md
- /memories/{applicant_name}/{applicant_name}_risk_calculation.md

Synthesize these findings into a final decision.
"""
```

### Memory Cleanup

Clean up old memories before new runs:

```python
# In orchestrator workflow
"""
Before processing:
1. Delete any existing files in /memories/{applicant_name}/
2. Start fresh to avoid confusion from previous runs
"""
```

---

## Advanced Features

### 1. Model Configuration

```python
model = init_chat_model(
    model="anthropic:claude-sonnet-4-5-20250929",
    temperature=0.0,  # Deterministic for reproducibility
    api_key=api_key,
)
```

**Key Settings:**
- **temperature=0.0** - Required for deterministic, reproducible decisions
- **Model choice** - Claude Sonnet 4.5 recommended for complex reasoning
- **API keys** - Managed through configuration (Pydantic settings)

### 2. Parallel Sub-Agent Execution

The framework supports parallel delegation:

```python
# Multiple sub-agents can run simultaneously
# when their tasks are independent
```

**Example:**
```
Research Query → 3 parallel sub-agents (compare X, Y, Z)
Wait for all → Synthesize findings
```

### 3. Strategic Reflection with think_tool

Enable deliberate pauses for analysis:

```python
@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """Record strategic reflection on progress.

    Args:
        reflection: Your detailed analysis of current state and next steps

    Returns:
        Confirmation that reflection was recorded
    """
    return f"Reflection recorded: {reflection}"
```

**Usage Pattern:**
```python
# After each major step
think_tool("""
Analysis: Successfully extracted loan data
Found: DTI inputs (income, debts, payment)
Gap: Still need policy threshold for comparison
Next: Query policy-agent for DTI max threshold
""")
```

### 4. Sub-Agent Isolation

Each sub-agent:
- Has **independent tool access** - Only sees its assigned tools
- Maintains **isolated context** - Cannot access orchestrator's state
- **Cannot invoke other sub-agents** - Must return to orchestrator
- Runs with **fresh context per delegation** - No memory between invocations

### 5. Type Safety

Tools are type-checked based on function signatures:

```python
@tool(parse_docstring=True)
def calculate(expression: str) -> str:
    # Framework validates expression is a string
    # Framework validates return is a string
    pass
```

---

## Execution Pattern

### Running a Deep Agent

```python
import asyncio
from utils.display_messages import stream_agent

async def process_loan(applicant_name: str):
    # Create the orchestrator
    agent = loan_orchestrator_create(applicant_name=applicant_name)

    # Create request
    request = f"Please process the auto loan application for {applicant_name}"

    # Stream response (live updates)
    await stream_agent(
        agent,
        {"messages": [{"role": "user", "content": request}]},
    )

# Run the orchestrator
asyncio.run(process_loan("Sarah Chen"))
```

### Streaming Agent Responses

```python
async def stream_agent(agent, query, config=None):
    """Stream agent execution with real-time updates."""
    async for graph_name, stream_mode, event in agent.astream(
        query,
        stream_mode=["updates", "values"],
        subgraphs=True,
        config=config
    ):
        if stream_mode == "updates":
            # Process agent messages
            node, result = list(event.items())[0]
            if "messages" in result:
                format_messages(result["messages"])
```

---

## This Project's Implementation

### Architecture

```
Orchestrator: loan_orchestrator
├── Sub-Agent 1: box-extract-agent
│   ├── Tools: search_loan_folder, list_loan_documents, ask_box_ai_about_loan
│   └── Output: Structured loan data extraction
│
├── Sub-Agent 2: policy-agent
│   ├── Tools: ask_box_ai_about_loan (for policies), think_tool
│   └── Output: Policy interpretations and thresholds
│
└── Sub-Agent 3: risk-calculation-agent
    ├── Tools: calculate, think_tool
    └── Output: Risk metrics and violation detection
```

### Memory Backend Configuration

```python
# Composite backend routes
CompositeBackend(
    default=StateBackend(rt),              # Ephemeral conversation state
    routes={
        "/memories/": FilesystemBackend(...)  # Persistent decision reports
    }
)
```

### Workflow Pattern

1. **Orchestrator receives request** - Process loan for applicant
2. **Delegate to box-extract-agent** - Extract all application data
3. **Delegate to policy-agent** - Retrieve underwriting thresholds
4. **Delegate to risk-calculation-agent** - Calculate metrics and violations
5. **Orchestrator synthesizes** - Review findings, make decision
6. **Orchestrator writes reports** - Generate comprehensive documentation
7. **Orchestrator uploads to Box** - Store decision in applicant folder

---

## Dependencies

**Core Framework:**
- `deepagents` (≥0.3.0) - Deep Agents framework
- `langgraph` (≥1.0.4) - Graph-based agent orchestration
- `langchain-anthropic` (≥1.2.0) - Claude model integration
- `langchain-core` - Tool definitions and base classes

**Configuration:**
- `pydantic` (≥2.12.5) - Data validation
- `pydantic-settings` (≥2.12.0) - Environment-based config

---

## Key Files in This Project

**Framework Implementation:**
- [src/agents/loan_orchestrator.py](../src/agents/loan_orchestrator.py) - Main orchestrator factory
- [src/agents/orchestrator_research.py](../src/agents/orchestrator_research.py) - Research agent (reference)
- [src/agents/loan_underwriting/loan_tools.py](../src/agents/loan_underwriting/loan_tools.py) - Tool definitions
- [src/agents/loan_underwriting/loan_prompts.py](../src/agents/loan_underwriting/loan_prompts.py) - System prompts

**Configuration:**
- [src/app_config.py](../src/app_config.py) - Pydantic settings
- [pyproject.toml](../pyproject.toml) - Dependencies

**Demo Scripts:**
- [src/demo_loan.py](../src/demo_loan.py) - Loan orchestrator demo
- [src/demo_research.py](../src/demo_research.py) - Research agent demo

---

## Further Reading

- **LangChain Deep Agents Documentation** - Consult the MCP server for detailed API docs
- **LangGraph Documentation** - Understanding state graphs and workflow orchestration
- **Research Agent Reference** - See [src/agents/orchestrator_research.py](../src/agents/orchestrator_research.py) for a simpler example

---

## Summary

Deep Agents provides a powerful framework for building multi-agent systems:

- **Orchestrator pattern** - Coordinate workflows with specialized sub-agents
- **Flexible memory** - Mix ephemeral and persistent storage
- **Tool integration** - Seamless LangChain tool system
- **Isolated contexts** - Sub-agents maintain independent state
- **Type safety** - Automatic validation of tool parameters
- **Parallel execution** - Run independent sub-agents concurrently

This project demonstrates these capabilities through automated loan underwriting, coordinating document extraction, policy interpretation, and risk calculation into a cohesive decision-making system.
