import asyncio
import os
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Ensure Google Cloud Project and Location are set
# These should be in your .env file or set as environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")
use_vertex_ai = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "False").lower() == "true"

if not project_id or not location:
    raise ValueError("GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set in .env or environment variables.")

# Import the agent you want to test
# Example: Testing the find_and_navigate_agent
from app.agents.workflow_agents import find_and_navigate_agent

async def run_test_agent():
    app_name = "test_app"
    user_id = "test_user"
    session_id = "test_session_123"

    session_service = InMemorySessionService()
    # Create a new session for each test run
    session = await session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id)

    runner = Runner(
        agent=find_and_navigate_agent, # Specify the agent to test
        app_name=app_name,
        session_service=session_service
    )

    print(f"Running test with agent: {find_and_navigate_agent.name}")
    query = "Where can I find good Char Kuey Teow in Penang and how do I get there from Komtar?"
    print(f"Query: {query}")

    user_message = types.Content(role='user', parts=[types.Part(text=query)])

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=user_message):
        if event.is_final_response() and event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")
        # You can add more logging here to see intermediate events

    # Optionally, inspect the final session state
    final_session = await session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
    print("\nFinal Session State:")
    import json
    print(json.dumps(final_session.state, indent=2))

if __name__ == "__main__":
    asyncio.run(run_test_agent())

#python test_agent.py