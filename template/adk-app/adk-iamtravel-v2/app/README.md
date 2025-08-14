# IamTravel - A Multi-Agent Travel Assistant

This application is a multi-agent travel assistant built with the Google Agent Development Kit (ADK). It uses a team of specialized agents to handle various travel-related queries, from finding restaurants and events to planning complex, multi-step itineraries.

## Application Architecture

The application is designed around a central **Router Agent** that delegates tasks to a team of specialist agents. This modular architecture makes the system scalable and easy to maintain.

The agent team includes:
- **`foodie_agent`**: Finds the best restaurants based on user queries.
- **`transportation_agent`**: Provides directions to a given destination.
- **`weekend_guide_agent`**: Finds local events and activities for a specific weekend.
- **`planner_agent`**: Proposes initial trip itineraries.
- **`critic_agent`**: Critiques and refines travel plans based on constraints.
- **`refiner_agent`**: Improves plans based on the critic's feedback.
- **`museum_finder_agent`**: Finds museums.
- **`concert_finder_agent`**: Finds concerts.
- **`synthesis_agent`**: Combines results from multiple agents into a single summary.

These agents are orchestrated using ADK's powerful workflow agents:
- **`SequentialAgent`**: For multi-step tasks like finding a place and then getting directions.
- **`LoopAgent`**: For iterative tasks like planning and refining an itinerary until it meets certain criteria.
- **`ParallelAgent`**: For running multiple searches concurrently to improve efficiency.

## File Structure

The application is organized into the following file structure:

```
app/
├── __init__.py
├── agent.py
├── agents/
│   ├── __init__.py
│   ├── llm_agents.py
│   ├── workflow_agents.py
│   └── router_agent.py
├── tools/
│   ├── __init__.py
│   └── exit_loop_tool.py
├── utils/
│   ├── __init__.py
│   └── session_manager.py
├── main.py
└── README.md
```

- **`__init__.py`**: Initializes directories as Python packages.
- **`agent.py`**: This file serves as the primary entry point for `adk web`. It imports and exposes the `root_agent` from its modular location.
- **`agents/`**: Contains definitions for all agents.
    - **`llm_agents.py`**: Defines individual LLM-powered agents (`Agent`).
    - **`workflow_agents.py`**: Defines workflow agents (`SequentialAgent`, `LoopAgent`, `ParallelAgent`) that orchestrate other agents.
    - **`router_agent.py`**: Defines the `root_agent` which acts as the main router.
- **`tools/`**: Contains definitions for custom tools.
    - **`exit_loop_tool.py`**: Defines the `exit_loop` tool used in iterative planning.
    - **`my_google_search_tool.py`**: Defines the `googlesearch_agent` which provides Google search capabilities.
- **`utils/`**: Contains utility functions and session management.
    - **`session_manager.py`**: Manages ADK sessions and provides a helper function to run agent queries.
- **`main.py`**: Contains example usage of the `root_agent` for direct execution (e.g., for testing specific flows).
- **`README.md`**: This file, providing documentation for the application.

## How to Run Locally with `adk-web`

To run the application locally for development and testing, you will use Google Cloud's Vertex AI for model access.

1.  **Install Dependencies**:
    Make sure you have `google-adk` and `google-cloud-aiplatform` installed.
    ```bash
    pip install google-adk google-cloud-aiplatform python-dotenv
    ```

2.  **Set up your Google Cloud Environment**:
    *   **Authenticate**: Ensure you are authenticated to Google Cloud and have Application Default Credentials (ADC) set up.
        ```bash
        gcloud auth application-default login
        ```
    *   **Configure Project and Location**: Create a `.env` file in the `adk-iamtravel-v2` directory with the following content. Replace placeholders with your actual Google Cloud Project ID and desired Vertex AI location (e.g., `us-central1`).
        ```
        GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
        GOOGLE_CLOUD_LOCATION="YOUR_VERTEX_AI_LOCATION"
        GOOGLE_GENAI_USE_VERTEXAI="TRUE"
        ```

3.  **Run the Dev UI**:
    Navigate to the `adk-iamtravel-v2` directory in your terminal and run:
    ```bash
    adk web
    ```
    This will start a local web server. Open the provided URL (usually `http://localhost:8000`) in your browser to access the ADK Dev UI. From there, you can select the `router_agent` and interact with it.

## Deploying to a Local FastAPI Server

For more custom local deployment scenarios, you can run the agent using a FastAPI server. A pre-configured script `fastapi_server.py` is provided in the project root.

1.  **Install FastAPI and Uvicorn**:
    If you haven't already, install the necessary packages:
    ```bash
    pip install fastapi uvicorn
    ```

2.  **Run the FastAPI Server**:
    Navigate to the `adk-iamtravel-v2` directory in your terminal and run:
    ```bash
    uvicorn fastapi_server:app --host 0.0.0.0 --port 8000
    ```
    This will start the FastAPI server, making your agents accessible via HTTP requests at `http://localhost:8000`.

## Interacting with the Local API Server Programmatically

Once either the `adk web` server or the FastAPI server is running, you can interact with your agents programmatically via HTTP requests. This is useful for integrating with other applications or for automated testing.

1.  **Ensure a Local Server is Running**:
    Follow the steps in "How to Run Locally with `adk-web`" or "Deploying to a Local FastAPI Server" to start a server.

2.  **Create a Python Client Script**:
    Create a new Python file, for example, `api_client.py`, in the root of your project (`adk-iamtravel-v2/`).

    ```python
    # api_client.py
    import requests
    import json

    # Configuration
    BASE_URL = "http://localhost:8000"
    APP_NAME = "router_agent" # The name of your root agent/application
    USER_ID = "api-test-user"
    SESSION_ID = "api-test-session-123"

    async def interact_with_agent(query: str):
        # 1. Create a session (if it doesn't exist)
        session_url = f"{BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}"
        response = requests.post(session_url)
        if response.status_code == 200:
            print(f"Session created/retrieved: {response.json()}")
        else:
            print(f"Failed to create/retrieve session: {response.status_code} - {response.text}")
            return

        # 2. Send a query
        run_url = f"{BASE_URL}/run"
        payload = {
            "app_name": APP_NAME,
            "user_id": USER_ID,
            "session_id": SESSION_ID,
            "new_message": {
                "role": "user",
                "parts": [{
                    "text": query
                }]
            }
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(run_url, headers=headers, data=json.dumps(payload), stream=True)

        print("\nAgent Response (streaming):")
        full_response_text = ""
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                try:
                    # Assuming each chunk is a complete JSON object for simplicity
                    # In a real-world scenario, you might need to buffer and parse incomplete JSON
                    event = json.loads(chunk.decode('utf-8'))
                    if event.get("type") == "final_response" and event.get("content") and event["content"].get("parts"):
                        text_part = event["content"]["parts"][0].get("text", "")
                        print(text_part, end='')
                        full_response_text += text_part
                except json.JSONDecodeError:
                    print(f"Could not decode JSON chunk: {chunk.decode('utf-8')}")

        print("\n\nInteraction complete.")

    if __name__ == "__main__":
        import asyncio
        # Example usage
        asyncio.run(interact_with_agent("Find me the best sushi in Palo Alto and then tell me how to get there from the Caltrain station."))
        # asyncio.run(interact_with_agent("Hi"))
    ```

3.  **Run the Client Script**:
    Make sure a local server is running in a separate terminal, then execute your client script:

    ```bash
    python api_client.py
    ```

    This script will send a request to your local ADK server and print the agent's response.

## Sample Chat Flows

This section provides sample questions to explore the capabilities of each agent and observe the routing behavior of the `root_agent`.

*   **Greeting Agent (`greeting_agent`)**
    *   **Query**: "Hi"
    *   **Expected Agent**: `greeting_agent`
    *   **Explanation**: Handles general greetings and simple conversational queries.

*   **Foodie Agent (`foodie_agent`)**
    *   **Query**: "Find me the best Nasi Lemak restaurant in Kuala Lumpur."
    *   **Expected Agent**: `foodie_agent`
    *   **Explanation**: Specifically designed for queries about finding a single food place.

*   **Find and Navigate Agent (`find_and_navigate_agent`)**
    *   **Query**: "Where can I find good Char Kuey Teow in Penang and how do I get there from Komtar?"
    *   **Expected Agent**: `find_and_navigate_agent`
    *   **Explanation**: Handles queries that involve first finding a location and then getting directions to it.

*   **Iterative Planner Agent (`iterative_planner_agent`)**
    *   **Query**: "Plan a trip to Kuala Lumpur. I want to visit the Petronas Twin Towers and eat at a restaurant nearby. The total travel time between the two should be short."
    *   **Expected Agent**: `iterative_planner_agent`
    *   **Explanation**: Orchestrates planning and refinement based on specific constraints (like travel time).

*   **Parallel Planner Agent (`parallel_planner_agent`)**
    *   **Query**: "Plan a weekend in Kuala Lumpur. I want to visit the National Museum, see a performance at Istana Budaya, and eat at a nice restaurant."
    *   **Expected Agent**: `parallel_planner_agent`
    *   **Explanation**: Designed for queries that require finding multiple, independent things concurrently and then summarizing the results.

*   **Day Trip Agent (`day_trip_agent`)**
    *   **Query**: "Plan a day trip to Port Dickson from Kuala Lumpur."
    *   **Expected Agent**: `day_trip_agent`
    *   **Explanation**: A general planner for any other simple day trip requests that don't fit the more specific agent criteria.

## How to Deploy to Google Cloud Run

You can deploy this agent as a containerized application to Google Cloud Run.

1.  **Prerequisites**:
    - A Google Cloud Project with billing enabled.
    - The [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and configured.

2.  **Create a `Dockerfile`**:
    In the `app` directory, create a `Dockerfile` with the following content:

    ```Dockerfile
    # Use an official Python runtime as a parent image
    FROM python:3.11-slim # Using a more recent stable Python version

    # Set the working directory in the container
    WORKDIR /usr/src/app

    # Copy the current directory contents into the container at /usr/src/app
    COPY . .

    # Install any needed packages
    RUN pip install --no-cache-dir google-adk google-cloud-aiplatform uvicorn python-dotenv

    # Make port 8080 available to the world outside this container
    EXPOSE 8080

    # Define environment variables for Vertex AI access
    ENV GOOGLE_GENAI_USE_VERTEXAI="TRUE"

    # Run app.agent when the container launches
    CMD ["uvicorn", "app.agent:root_agent", "--host", "0.0.0.0", "--port", "8080"]
    ```

3.  **Build and Push the Docker Image**:
    From the `adk-iamtravel-v2` directory, build the Docker image and push it to Google Container Registry (GCR). Replace `[your-gcp-project-id]` with your actual project ID.

    ```bash
    export PROJECT_ID=[your-gcp-project-id]
    export IMAGE_NAME=iamtravel-agent
    export IMAGE_TAG=gcr.io/${PROJECT_ID}/${IMAGE_NAME}:latest

    gcloud builds submit --tag ${IMAGE_TAG} .
    ```

4.  **Deploy to Cloud Run**:
    Deploy the container image to Cloud Run. Replace `[your-gcp-project-id]` and `YOUR_VERTEX_AI_LOCATION` with your actual values.

    ```bash
    gcloud run deploy ${IMAGE_NAME} \
      --image=${IMAGE_TAG} \
      --platform=managed \
      --region=YOUR_VERTEX_AI_LOCATION \
      --allow-unauthenticated \
      --set-env-vars="GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_CLOUD_LOCATION=${YOUR_VERTEX_AI_LOCATION},GOOGLE_GENAI_USE_VERTEXAI=TRUE"
    ```
    When prompted, confirm the deployment. Once the deployment is complete, you will get a service URL.

## How to Test the Deployment with `curl`

You can test your deployed agent using `curl` from your local machine.

1.  **Get the Service URL**:
    You can get the URL of your deployed service from the output of the `gcloud run deploy` command or by running:
    ```bash
    gcloud run services describe iamtravel-agent --platform=managed --region=YOUR_VERTEX_AI_LOCATION --format='value(status.url)'
    ```

2.  **Create a Session**:
    First, create a session with the agent. Replace `[your-service-url]` with the URL obtained above.

    ```bash
    export SERVICE_URL=[your-service-url]
    curl -X POST ${SERVICE_URL}/apps/router_agent/users/test-user/sessions/test-session
    ```

3.  **Send a Query**:
    Now, send a query to the agent.

    ```bash
    curl -X POST ${SERVICE_URL}/run \
      -H "Content-Type: application/json" \
      -d 
      {
        "app_name": "router_agent",
        "user_id": "test-user",
        "session_id": "test-session",
        "new_message": {
          "role": "user",
          "parts": [{
            "text": "Find me the best sushi in Palo Alto and then tell me how to get there from the Caltrain station."
          }]
        }
      }
    ```
    You should receive a JSON response containing the agent's final answer.

## Testing Specific Agents Locally

You can test individual agents or workflows directly using a Python script, which is useful for debugging and focused testing without the `adk web` UI.

1.  **Test Script Location**:
    The test script `test_agent.py` is located in the root directory of this project (`adk-iamtravel-v2/`).

2.  **Run the Test Script**:
    From your project root directory (`adk-iamtravel-v2/`), execute the script:

    ```bash
    python test_agent.py
    ```

    This will run the `find_and_navigate_agent` (or whichever agent is configured in `test_agent.py`) directly and print its output to the console. You can modify `test_agent.py` to test other agents by changing the imported agent and the query.