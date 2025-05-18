from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types  # Para criar conteúdos (Content e Part)

from datetime import date
import textwrap # Para formatar melhor a saída de texto
from IPython.display import display, Markdown # Para exibir texto formatado no Colab
import requests # Para fazer requisições HTTP
import warnings


warnings.filterwarnings("ignore")
class CallAgent:
  # Função auxiliar que envia uma mensagem para um agente via Runner e retorna a resposta final
  def call_agent(agent: Agent, message_text: str) -> str:
        # Cria um serviço de sessão em memória
        session_service = InMemorySessionService()
        # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)
        session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
        # Cria um Runner para o agente
        runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
        # Cria o conteúdo da mensagem de entrada
        content = types.Content(role="user", parts=[types.Part(text=message_text)])
    
        final_response = ""
        # Itera assincronamente pelos eventos retornados durante a execução do agente
        for event in runner.run(user_id="user1", session_id="session1", new_message=content):
            if event.is_final_response():
              for part in event.content.parts:
                if part.text is not None:
                  final_response += part.text
                  final_response += "\n"
        return final_response

  #"""Responsável por fornecer informações e dicas sobre cuidados com o recém-nascido."""    
  def get_newborn_care_info(topico):

        take_care = Agent(
            name="newborn_care",
            model="gemini-2.5-flash-preview-04-17",
            description="Agente especializado em cuidados com recém-nascidos",
            tools=[google_search],
            instruction="""
            Você é um assistente de pesquisa. A sua tarefa é fornecer informações sobre cuidados relevantes com recém-nascidos. Use a 
            ferramenta de busca do google (google_search) para recuperar informações caso necessário.
            Foque em dados sobre amamentação, sono seguro e bem-estar do bebê.
            Utilize fontes confiáveis e atualizadas para fornecer as melhores informações.
            """ 
        )

        ret = CallAgent.call_agent(take_care, topico)
        return ret

  #"""Responsável por monitorar e fornecer informações sobre o desenvolvimento do bebê."""
  def get_development_info(context):
        # Logic to provide development information for the age
        development_agent = Agent(
            name="development_tracking",
            model="gemini-2.5-flash-preview-04-17",
            description="Agente especializado em rastreamento do desenvolvimento infantil",
            tools=[google_search],
            instruction="""
            Você é um assistente de pesquisa. A sua tarefa é forncer informações relevantes sobre o desenvolvimento infantil. Use a ferramenta de busca do 
            google (google_search) para recuperar informações caso necessário.
            Foque em dados sobre marcos de desenvolvimento, atividades de estimulação, bem-estar da criança, régua de desenvolvimento e saúde do bebê.
            Crie um gráfico em html para exibir os marcos de desenvolvimento e uma tabela para exibir a cartilha de vacinação.
            """
        )
        

        return CallAgent.call_agent(development_agent, context)

  #"""Responsável por fornecer informações e dicas durante a gestação."""
  def get_gestation_tracking_info(context):
        gestation_tracking_agent = Agent(
            name="gestation_tracking",
            model="gemini-2.0-flash",
            description="Agente especializado em rastreamento de gestação",
            tools=[google_search],
            instruction="""
            Você é um assistente de pesquisa. A sua tarefa é usar a ferramenta de busca do google (google_search) para recuperar informações muito relevantes sobre
            o período gestacional.
            Foque em dados sobre o desenvolvimento do feto, saúde da mãe e dicas de bem-estar.
            Este agente é especializado em fornecer informações precisas e atualizadas sobre a gestação.
            """
        )

        # Logic to fetch relevant information for the gestation week
        ret = CallAgent.call_agent(gestation_tracking_agent, context)

        return ret

  #"""Responsável por fornecer informações e suporte para os pais sobre locais de atendimento e serviços de saúde."""
  def get_health_info(context):
        # Logic to fetch answers for common questions
      first_time_parent_agent = Agent(
                  name="first_time_parent",
                  model="gemini-2.0-flash",
                  description="Agente especializado em fornecener informações sobre profissionais de saúde e serviços de saúde",
                  tools=[google_search],
                  instruction="""
                  Você é um assistente de pesquisa. A sua tarefa é fornecer informações sobre localização de serviços de saúde e profissionais de saúde. Utilize a
                  ferramenta de busca do google (google_search) para recuperar informações muito relevantes sobre serviços de saúde e profissionais de saúde.
                  Foque em dados sobre pediatras, enfermeiros, hospitais e clínicas.
                  """
            )

      return CallAgent.call_agent(first_time_parent_agent, context)

  #"""Responsável por Refinar os dados a serem apresentados."""
  def get_analysis_care(context, data=None):
        # AI logic to analyze the context and data and provide a suggestion
        # This would be the most complex component, involving machine learning or specialized rules
        analysis_agent = Agent(
            name="analysis_care",
            model="gemini-2.0-flash",
            description="Agente especializado em refinar os dados sobre cuidados do recém-nascido e gestação",
            tools=[],
            instruction="""
            Você é um assistente de refinamento de dados. A sua tarefa é analisar os dados fornecidos e fornecer sugestões sobre cuidados com recém-nascidos e gestação.
            Formate os dados de entrada para que sejam mais compreensíveis e úteis, mantenha os dados e endereços dos locais relevantes.
            Considere fazer alterações na abordagem de cuidados ou fornecer informações adicionais que possam ser úteis.
            O resultado deve ser apresentado de forma clara e organizada, facilitando a compreensão e a aplicação das informações.
            """
        )
        context = f"Contexto: {context}"
        return CallAgent.call_agent(analysis_agent, context)