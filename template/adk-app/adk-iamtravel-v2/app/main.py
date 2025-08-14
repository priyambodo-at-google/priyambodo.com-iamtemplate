import asyncio
from app.agents.router_agent import root_agent
from app.utils.session_manager import run_agent_query, session_service, my_user_id

async def main():
    # Example usage of the router agent
    session = await session_service.create_session(app_name="my_travel_app", user_id=my_user_id)

    print("\n--- Testing Router Agent ---")
    await run_agent_query(
        agent=root_agent,
        query="Find me a good Italian restaurant in New York City.",
        session=session,
        user_id=my_user_id,
        is_router=True
    )

    await run_agent_query(
        agent=root_agent,
        query="Find me a good Italian restaurant in New York City and give me directions from Times Square.",
        session=session,
        user_id=my_user_id,
        is_router=True
    )

    await run_agent_query(
        agent=root_agent,
        query="Plan a trip to San Francisco. I want to visit a museum, see a concert, and eat at a nice restaurant.",
        session=session,
        user_id=my_user_id,
        is_router=True
    )

    await run_agent_query(
        agent=root_agent,
        query="Plan a day trip to a beach near Los Angeles.",
        session=session,
        user_id=my_user_id,
        is_router=True
    )

    await run_agent_query(
        agent=root_agent,
        query="Plan a trip to London. I want to visit the British Museum and eat at a restaurant nearby. The total travel time between the two should be short.",
        session=session,
        user_id=my_user_id,
        is_router=True
    )

if __name__ == "__main__":
    asyncio.run(main())
