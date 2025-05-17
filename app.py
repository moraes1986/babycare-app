import os
from google import genai
from src.model.utils.ia_agents.gestation_tracking import GestationTrackingAgent

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the Google GenAI client
genai_client = genai.Client(api_key=GOOGLE_API_KEY)
# Set the API key for the client
genai_client.api_key = GOOGLE_API_KEY
# Example usage
# Fetch information for gestation week 20
# This will call the gestation tracking agent and print the information for week 20
# Note: The actual implementation of the agent and its methods would be in the respective files.

class __main__:
    def __init__(self):
        pass
    def run(self):
        # Example usage
        # Fetch information for gestation week 20
        # This will call the gestation tracking agent and print the information for week 20
        # Note: The actual implementation of the agent and its methods would be in the respective files.
        print(GestationTrackingAgent.get_gestation_tracking_info(20), "Gestation week: 20")
if __name__ == "__main__":
    main = __main__()
    main.run()
