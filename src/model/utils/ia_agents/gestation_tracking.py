from google.adk.agents import Agent
from google.adk.tools import google_search
from .agent import CallAgent



class GestationTrackingAgent:
    """Responsible for providing information and tips during gestation."""
    def get_gestation_tracking_info(gestation_week):
        gestation_tracking_agent = Agent(
            name="gestation_tracking",
            model="gemini-2.0-flash",
            description="Agente especializado em rastreamento de gestação",
            tools=[google_search],
            instruction="""
            Você é um assistente de pesquisa. A sua tarefa é usar a ferramenta de busca do google (google_search) para recuperar informações muito relevantes sobre
            o período de gestacional.
            Foque em dados sobre o desenvolvimento do feto, saúde da mãe e dicas de bem-estar.
            Este agente é especializado em fornecer informações precisas e atualizadas sobre a gestação.
            """
        )
        input = f"Semana da gestação: {gestation_week}"
        # Logic to fetch relevant information for the gestation week
        ret = CallAgent.call_agent(gestation_tracking_agent, input)

        return ret