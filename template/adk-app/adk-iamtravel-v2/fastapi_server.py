import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import StreamingResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json

# Load environment variables from .env file
load_dotenv()

# Ensure Google Cloud Project and Location are set
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")
use_vertex_ai = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "False").lower() == "true"

if not project_id or not location:
    raise ValueError("GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set in .env or environment variables.")

# Import the main agent (e.g., router_agent)
from app.agents.router_agent import router_agent

app = FastAPI()

session_service = InMemorySessionService()

@app.post("/apps/{app_name}/users/{user_id}/sessions/{session_id}")
async def create_or_get_session(
    app_name: str,
    user_id: str,
    session_id: str,
):
    """Creates or retrieves a session."""
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        return {"message": "Session created or retrieved successfully", "session_id": session.session_id}
    except Exception as e:
        return Response(content=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/run")
async def run_agent(request: Request):
    """Runs the agent with a new message and streams events."""
    try:
        body = await request.json()
        app_name = body.get("app_name")
        user_id = body.get("user_id")
        session_id = body.get("session_id")
        new_message_data = body.get("new_message")

        if not all([app_name, user_id, session_id, new_message_data]):
            return Response(content="Missing required fields", status_code=status.HTTP_400_BAD_REQUEST)

        new_message = types.Content(
            role=new_message_data.get("role"),
            parts=[types.Part(text=p.get("text")) for p in new_message_data.get("parts", [])]
        )

        runner = Runner(
            agent=router_agent, # Use the main router agent
            app_name=app_name,
            session_service=session_service
        )

        async def event_generator():
            async for event in runner.run_async(
                user_id=user_id, session_id=session_id, new_message=new_message
            ):
                yield json.dumps(event.model_dump(mode='json')) + "\n"

        return StreamingResponse(event_generator(), media_type="application/json")

    except Exception as e:
        return Response(content=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
