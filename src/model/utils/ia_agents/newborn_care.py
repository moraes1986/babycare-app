from google.adk.agents import Agent
from google.adk.tools import google_search
from .agent import CallAgent

class NewbornCareAgent:
    """Responsável por fornecer informações e dicas sobre cuidados com o recém-nascido."""

    def get_newborn_care_info(topico):

        take_care = Agent(
            name="newborn_care",
            model="gemini-2.0-flash",
            description="Agente especializado em cuidados com recém-nascidos",
            tools=[google_search],
            instruction="""
            Você é um assistente de pesquisa. A sua tarefa é fornecer informações sobre cuidados com recém-nascidos.
            Foque em dados sobre amamentação, sono seguro e bem-estar do bebê.
            Este agente é especializado em fornecer informações precisas e atualizadas sobre cuidados com recém-nascidos.
            """ 
        )

        ret = CallAgent.call_agent(take_care, topico)
        return ret