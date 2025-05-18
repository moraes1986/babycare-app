import os
from google import genai

from src.model.entities.baby import Baby
from src.model.entities.user import User
from src.model.utils.agents_especialists import CallAgent


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

        
        # Initialize the user and baby objects
        user = User(name='', age=0, city='', state='')

        user.name = input('Qual é o seu nome? \n')
        user.age = input('Qual é a sua idade? \n')
        user.city = input('Qual é a sua cidade? \n')
        user.state = input('Qual é o seu estado? ex.: SP \n')

        is_gestation = input('Você está grávida? (sim/não) \n').lower()

        if is_gestation == 'sim':
            user.week_gestation = input('Qual é a semana de gestação?')

            # Call the gestation tracking agent
            context = str(f'Olá meu nome é {user.name}, tenho {user.age} e estou grávida de {user.week_gestation} semanas.')
            print(context)
            gestation_info = CallAgent.get_gestation_tracking_info(context)
            print(f'-------------------------------- Informação Gestacional -----------------------------\n')
            print(gestation_info)
            
            development_info = CallAgent.get_health_info(f'Estou em {user.city}-{user.state}, me ajude com informações sobre pronto de socorro próximo e profissionais de saúde.')
            print(f'\n-------------------------------- Informação de Desenvolvimento -----------------------------\n')
            print(development_info)

            refinement_info = CallAgent.get_analysis_care(f'{gestation_info} \n {development_info}')
            print(f'\n-------------------------------- Informação de Refinamento -----------------------------\n')
            print(refinement_info)


        else:
            print("Você não está grávida.")
            baby = Baby(name='', age=0)
        # Assuming the user is not pregnant, we can skip the gestation tracking part
        # If the user is pregnant, we can ask for the baby's name and birth date
        # and proceed with the gestation tracking


            baby.name = input('Qual é o nome do seu bebê? \n')
            baby.age = input('Qual é a idade do seu bebê? \n')

            # Call the gestation tracking agent
            context = str(f'Olá meu nome é {user.name}, tenho {user.age} e sou mãe do(a) {baby.name} de {baby.age} ano(s).')
            print(context)
            newborn_info = CallAgent.get_newborn_care_info(context)
            print(f'-------------------------------- Informação Mamãe e Bebê -----------------------------\n')
            print(newborn_info)

            development_info = CallAgent.get_development_info(f'A/O bebê {baby.name} de {baby.age} ano(s).')
            print(f'\n-------------------------------- Informação de Desenvolvimento -----------------------------\n')
            print(development_info)

            health_info = CallAgent.get_health_info(f'Estou em {user.city}-{user.state}, me ajude com informações sobre pronto de socorro próximo e profissionais de saúde.')
            print(f'\n-------------------------------- Informação de Saúde -----------------------------\n')
            print(health_info)

            refinement_info = CallAgent.get_analysis_care(f'{newborn_info} \n {development_info} \n {health_info}')
            print(f'\n-------------------------------- Informação de Refinamento -----------------------------\n')
            print(refinement_info)

if __name__ == "__main__":
    main = __main__()
    main.run()
