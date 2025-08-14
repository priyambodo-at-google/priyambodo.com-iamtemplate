from google.adk.agents import Agent
from app.agents.llm_agents import day_trip_agent, foodie_agent_for_router, greeting_agent
from app.agents.workflow_agents import find_and_navigate_agent, iterative_planner_agent, parallel_planner_agent

root_agent = Agent(
    name="router_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a master request router. Your job is to analyze a user's query and decide which of the following agents or workflows is best suited to handle it.
    Do not answer the query yourself, only delegate to the most appropriate choice.

    Available Options:
    - 'greeting_agent': For general greetings and simple conversational queries.
    - 'foodie_agent': For queries *only* about finding a single food place.
    - 'find_and_navigate_agent': For queries that ask to *first find a place* and *then get directions* to it.
    - 'iterative_planner_agent': For planning a trip with a specific constraint that needs checking, like travel time.
    - 'parallel_planner_agent': For queries that ask to find multiple, independent things at once (e.g., a museum AND a concert AND a restaurant).
    - 'day_trip_agent': A general planner for any other simple day trip requests.

    Delegate to the single, most appropriate option.
    """,
    sub_agents=[
        greeting_agent,
        day_trip_agent,
        foodie_agent_for_router,
        find_and_navigate_agent,
        iterative_planner_agent,
        parallel_planner_agent,
    ]
)