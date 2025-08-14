# ADK Framework Best Practices

This document outlines best practices for building robust, scalable, and maintainable AI agents using the Google Agent Development Kit (ADK). The principles and examples are drawn from this application's implementation and the official ADK documentation.

## 1. Architect with a Central Router Agent

A core best practice for managing multi-agent systems is to use a central "Router Agent." This agent's sole responsibility is to analyze incoming requests and delegate them to the appropriate specialized sub-agent. This pattern promotes modularity and a clean separation of concerns.

**Example (`app/agents/router_agent.py`):**

Our application uses a `root_agent` that decides whether a query is from a customer or the shop owner and routes it accordingly.

```python
from google.adk.agents import Agent
from app.agents.llm_agents import customer_agent, owner_agent

root_agent = Agent(
    name="router_agent",
    model="gemini-1.5-flash",
    instruction="""You are a master request router for a bike shop assistant.
    Analyze the user's query to determine if it's from a customer or the owner.

    - If the query is about buying a bike, getting recommendations, or planning a ride, delegate to the 'customer_agent'.
    - If the query is about sales data, inventory levels, regional performance, or purchase orders, delegate to the 'owner_agent'.

    Do not answer the query yourself, only delegate.
    """,
    sub_agents=[
        customer_agent,
        owner_agent,
    ]
)
```

**Benefits:**
- **Maintainability:** Each agent has a single, well-defined purpose.
- **Scalability:** It's easy to add new capabilities by adding new specialized agents and updating the router's instructions.
- **Clarity:** The top-level logic is simple and easy to understand.

## 2. Crafting Effective LLM Agents

The power of an `LlmAgent` lies in its configuration. Follow these guidelines to create effective agents.

### a. Write Powerful Instructions

The `instruction` parameter is the most critical part of an agent's definition. It defines the agent's persona, goal, constraints, and behavior.

**Best Practices for Instructions:**
- **Define a Persona:** Give the agent a clear role (e.g., "You are ADK, a personal cycling assistant").
- **State the Goal:** Clearly articulate what the agent is supposed to achieve.
- **Provide Explicit Rules:** Set constraints and guidelines on how to handle different scenarios.
- **Guide Tool Usage:** Explain *when* and *why* to use specific tools.

**Example (`app/agents/llm_agents.py` - `customer_agent`):**

```python
customer_agent = Agent(
    name="customer_agent",
    model="gemini-1.5-flash",
    tools=[...],
    instruction="""You are ADK, a personal cycling assistant.
    Your goal is to help customers find the right bike and plan rides.
    Be friendly, conversational, and helpful.
    Follow the use cases provided in the instructions.
    - For bike recommendations, ask for riding style, skill level, and budget before suggesting a product.
    - After a purchase, offer to help plan a ride.
    - For ride planning, use the search tool to find trails and offer to send directions.
    """
)
```

### b. Equip Agents with Well-Defined Tools

Tools extend an agent's capabilities beyond the LLM's knowledge.

- **Atomic Functions:** Create tools as simple, single-purpose Python functions.
- **Descriptive Naming:** Use clear, descriptive names for your functions (e.g., `get_products`, `record_sale`).
- **Docstrings are Key:** The LLM uses the function's docstring to understand what the tool does. Write clear and concise docstrings that explain the tool's purpose and parameters.

**Example (`app/tools/data_store_tool.py`):**

```python
def get_products(category: str = None, skill_level: str = None, max_price: int = None):
    """
    Retrieves a list of products, optionally filtered by category, skill level, and maximum price.
    """
    # ... implementation ...
```

## 3. Organize Your Project for Clarity

A well-organized file structure is crucial for maintainability. This application follows a recommended structure for ADK projects.

```
app/
├── agents/         # Agent definitions (router, LLM, workflow)
├── tools/          # Tool definitions
├── utils/          # Utility functions (e.g., session management)
├── dummydata/      # Simulated database (CSVs)
├── dummyapi/       # Simulated API responses (JSON)
├── main.py         # Example usage and testing
└── agent.py        # Primary entry point for `adk web`
```

This separation ensures that concerns are neatly divided, making the codebase easier to navigate and manage.

## 4. Advanced Concepts

While our application uses a router and LLM agents, the ADK provides more advanced tools for complex orchestrations.

- **Workflow Agents:** For deterministic, multi-step processes, use `SequentialAgent`, `ParallelAgent`, or `LoopAgent` to control the execution flow without relying on an LLM for the orchestration logic itself.
- **Custom Agents:** For highly specific or unique workflows, you can inherit directly from `BaseAgent` to implement your own orchestration logic with full control over the execution flow.

Refer to the official ADK documentation (`llms-full.txt`) for detailed guides on implementing these advanced patterns.

## 5. DO NOT MODIFY THESE FILES

If I am not asking you to not use these files, do not update and do not refer to these files!
Files are : 
- README.md and 
- main.py
