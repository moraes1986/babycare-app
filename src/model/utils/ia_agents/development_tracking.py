from google.adk.agents import Agent
from google.adk.tools import google_search
from .agent import CallAgent

class DevelopmentTrackingAgent:
    """Responsável por monitorar e fornecer informações sobre o desenvolvimento do bebê."""

    def get_development_info(self, age_months):
        # Logic to provide development information for the age
        development_agent = Agent(
            name="development_tracking",
            model="gemini-2.0-flash",
            description="Agente especializado em rastreamento do desenvolvimento infantil",
            tools=[google_search],
            instruction="""
            Você é um assistente de pesquisa. A sua tarefa é fornecer informações sobre o desenvolvimento infantil.
            Foque em dados sobre marcos de desenvolvimento, atividades de estimulação e bem-estar da criança.
            Este agente é especializado em fornecer informações precisas e atualizadas sobre o desenvolvimento infantil bem como sugestões de atividades.
            """
        )
        input = f"Idade da criança: {age_months} meses"
        ret = CallAgent.call_agent(development_agent, input)

        return ret