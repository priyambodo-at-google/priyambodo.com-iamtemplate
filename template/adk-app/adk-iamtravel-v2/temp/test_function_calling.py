import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel, Part, Tool, FunctionDeclaration

load_dotenv() # Load environment variables from .env file

# Check for Vertex AI specific environment variables
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
location = os.environ.get("GOOGLE_CLOUD_LOCATION")

if not project_id or not location:
    print("Error: GOOGLE_CLOUD_PROJECT or GOOGLE_CLOUD_LOCATION not set in .env.")
    print("Please ensure these are in your .env file.")
    exit()

# Initialize Vertex AI
vertexai.init(project=project_id, location=location)

# Define a simple tool function
def get_current_weather(location: str):
    """Gets the current weather for the given location."""
    if location.lower() == "london":
        return {"location": "London", "temperature": "15C", "conditions": "Cloudy"}
    elif location.lower() == "new york":
        return {"location": "New York", "temperature": "25C", "conditions": "Sunny"}
    else:
        return {"location": location, "temperature": "N/A", "conditions": "Unknown"}

# Define the tool using FunctionDeclaration
get_current_weather_declaration = FunctionDeclaration(
    name="get_current_weather",
    description="Gets the current weather for a given location.",
    parameters={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "The city name"}
        },
        "required": ["location"],
    },
)

# Register the tool for Vertex AI
weather_tool = Tool(function_declarations=[get_current_weather_declaration])

try:
    # Use a model that supports tool calling (e.g., gemini-1.0-pro or gemini-1.5-flash for Vertex AI)
    # Ensure this model is available in your specified GOOGLE_CLOUD_LOCATION
    model = GenerativeModel("gemini-1.5-pro", tools=[weather_tool])

    # Attempt to invoke the tool via a prompt
    chat = model.start_chat()
    response = chat.send_message("What's the weather like in London?")

    print("Model Response:")
    if response.candidates:
        for part in response.candidates[0].content.parts:
            if part.function_call:
                print(f"  Function Call: {part.function_call.name}({part.function_call.args})")
                # Simulate tool execution and send result back
                tool_result = get_current_weather(**part.function_call.args)
                print(f"  Tool Result: {tool_result}")
                response_with_tool_result = chat.send_message(
                    Part.from_function_response(part.function_call.name, tool_result)
                )
                print(f"  Final Response after tool: {response_with_tool_result.text}")
            else:
                print(f"  Text: {part.text}")
    else:
        print("  No candidates found in the response.")

except Exception as e:
    print(f"\nAn error occurred during direct tool use test: {e}")
    print("This error indicates a problem with your Vertex AI setup, permissions, or the model's support for function calling.")
