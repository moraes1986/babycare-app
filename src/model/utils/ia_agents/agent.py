from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
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

