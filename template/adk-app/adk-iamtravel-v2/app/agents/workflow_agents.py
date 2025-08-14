from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent
from app.agents.llm_agents import foodie_agent_for_seq, transportation_agent, planner_agent, critic_agent, refiner_agent, museum_finder_agent, concert_finder_agent, restaurant_finder_agent_for_parallel, synthesis_agent

# The SequentialAgent to manage the find-and-navigate workflow.
find_and_navigate_agent = SequentialAgent(
    name="find_and_navigate_agent",
    sub_agents=[foodie_agent_for_seq, transportation_agent],
    description="A workflow that first finds a location and then provides directions to it."
)

# The LoopAgent orchestrates the critique-refine cycle
refinement_loop = LoopAgent(
    name="refinement_loop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=3
)

# The SequentialAgent puts it all together
iterative_planner_agent = SequentialAgent(
    name="iterative_planner_agent",
    sub_agents=[planner_agent, refinement_loop],
    description="A workflow that iteratively plans and refines a trip to meet constraints."
)

# The ParallelAgent runs all three specialists at once
parallel_research_agent = ParallelAgent(
    name="parallel_research_agent",
    sub_agents=[museum_finder_agent, concert_finder_agent, restaurant_finder_agent_for_parallel]
)

# The SequentialAgent runs the parallel search, then the synthesis
parallel_planner_agent = SequentialAgent(
    name="parallel_planner_agent",
    sub_agents=[parallel_research_agent, synthesis_agent],
    description="A workflow that finds multiple things in parallel and then summarizes the results."
)
