from google.adk.agents import Agent
from app.tools.exit_loop_tool import exit_loop, COMPLETION_PHRASE
from app.tools.my_google_search_tool import googlesearch_agent as search_tool

# This foodie_agent is specifically for the sequential workflow.
foodie_agent_for_seq = Agent(
    name="foodie_agent_for_seq",
    model="gemini-2.5-flash",
    #tools=[third_party_web_search],
    instruction="""You are an expert food critic. Your goal is to find the best restaurant based on a user's request.

    When you recommend a place, you must output *only* the name of the establishment and nothing else.
    For example, if the best sushi is at 'Jin Sho', you should output only: Jin Sho
    """,
    output_key="destination"  # ADK will save the agent's final response to state['destination']
)

# The transportation_agent reads from the shared state.
transportation_agent = Agent(
    name="transportation_agent",
    model="gemini-2.5-flash",
    tools=[search_tool],
    instruction="""You are a navigation assistant. Given a destination, provide clear directions.
    The user wants to go to: {destination}.

    Analyze the user's full original query to find their starting point.
    Then, provide clear directions from that starting point to {destination}.
    """,
)

weekend_guide_agent = Agent(
    name="weekend_guide_agent",
    model="gemini-2.5-flash",
    tools=[search_tool],
    instruction="You are a local events guide. Your task is to find interesting events, concerts, festivals, and activities happening on a specific weekend."
)

# Agent 1: Proposes an initial plan
planner_agent = Agent(
    name="planner_agent", model="gemini-2.5-flash", 
    #tools=[third_party_web_search],
    instruction="You are a trip planner. Based on the user's request, propose a single activity and a single restaurant. Output only the names, like: 'Activity: Exploratorium, Restaurant: La Mar'.",
    output_key="current_plan"
)

# Agent 2 (in loop): Critiques the plan
critic_agent = Agent(
    name="critic_agent", model="gemini-2.5-flash", 
    #tools=[third_party_web_search],
    instruction="""You are a logistics expert. Your job is to critique a travel plan. The user has a strict constraint: total travel time must be short.
    Current Plan: {current_plan}
    Use your tools to check the travel time between the two locations.
    IF the travel time is over 45 minutes, provide a critique, like: 'This plan is inefficient. Find a restaurant closer to the activity.'
    ELSE, respond with the exact phrase: 'The plan is feasible and meets all constraints.'""",

    output_key="criticism"
)

# Agent 3 (in loop): Refines the plan or exits
refiner_agent = Agent(
    name="refiner_agent", model="gemini-2.5-flash", 
    #tools=[third_party_web_search, exit_loop],
    tools=[exit_loop],
    instruction="""You are a trip planner, refining a plan based on criticism.
    Original Request: {session.query}
    Critique: {criticism}
    IF the critique is 'The plan is feasible and meets all constraints.', you MUST call the 'exit_loop' tool.
    ELSE, generate a NEW plan that addresses the critique. Output only the new plan names, like: 'Activity: de Young Museum, Restaurant: Nopa'.""",

    output_key="current_plan"
)

# Specialist Agent 1
museum_finder_agent = Agent(
    name="museum_finder_agent", model="gemini-2.5-flash", 
    tools=[search_tool],
    instruction="You are a museum expert. Find the best museum based on the user's query. Output only the museum's name.",
    output_key="museum_result"
)

# Specialist Agent 2
concert_finder_agent = Agent(
    name="concert_finder_agent", model="gemini-2.5-flash", 
    tools=[search_tool],
   instruction="You are an events guide. Find a concert based on the user's query. Output only the concert name and artist.",
    output_key="concert_result"
)

# A dedicated foodie agent for the parallel workflow
restaurant_finder_agent_for_parallel = Agent(
    name="restaurant_finder_agent_for_parallel",
    model="gemini-2.5-flash",
    #tools=[third_party_web_search],
    instruction="""You are an expert food critic. Your goal is to find the best restaurant based on a user's request.

    When you recommend a place, you must output *only* the name of the establishment.
    For example, if the best sushi is at 'Jin Sho', you should output only: Jin Sho
    """,
    output_key="restaurant_result" # Set the correct output key for this workflow
)

# Agent to synthesize the parallel results
synthesis_agent = Agent(
    name="synthesis_agent", model="gemini-2.5-flash",
    instruction="""You are a helpful assistant. Combine the following research results into a clear, bulleted list for the user.
    - Museum: {museum_result}
    - Concert: {concert_result}
    - Restaurant: {restaurant_result}
    """
)

day_trip_agent = Agent(
    name="day_trip_agent",
    model="gemini-2.5-flash",
    tools=[search_tool],
    instruction="You are a day trip planner. Your task is to create a simple day trip plan based on user's request."
)

# Create a standalone foodie_agent for direct delegation by the router.
foodie_agent_for_router = Agent(
    name="foodie_agent", # Keep the name the router expects
    model="gemini-2.5-flash",
    #tools=[googlesearch_agent],
    instruction="""You are an expert food critic. Your goal is to find the best restaurant based on a user's request.
    When you recommend a place, you must output *only* the name of the establishment and nothing else.
    For example, if the best sushi is at 'Jin Sho', you should output only: Jin Sho
    """,
    description="For queries *only* about finding a single food place."
)

greeting_agent = Agent(
    name="greeting_agent",
    model="gemini-2.5-flash",
    instruction="You are a friendly assistant. Respond to greetings and simple conversational queries.",
    description="For general greetings and simple conversational queries."
)