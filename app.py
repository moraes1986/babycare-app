import os
from google import genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS # Para permitir requisições de origens diferentes durante o desenvolvimento
from IPython.display import HTML, Markdown, display

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





# Supondo que suas classes User, Baby e CallAgent estão acessíveis
# Se elas estiverem em src/, certifique-se de que o Python possa encontrá-las
# (ex: adicionando src ao PYTHONPATH ou ajustando os imports)
# Para este exemplo, vou definir classes placeholder.
# SUBSTITUA PELAS SUAS DEFINIÇÕES REAIS!

# Placeholder para GOOGLE_API_KEY e genai client
# Você precisará configurar isso corretamente.
# import google.generativeai as genai

# genai.configure(api_key=GOOGLE_API_KEY)


app = Flask(__name__)
CORS(app) # Habilita CORS para todas as rotas

# Inicialização do cliente GenAI (faça isso uma vez globalmente)
# try:
#     genai_client = genai.Client(api_key=GOOGLE_API_KEY)
#     genai_client.api_key = GOOGLE_API_KEY
#     print("Cliente GenAI inicializado com sucesso.")
# except Exception as e:
#     print(f"Erro ao inicializar o cliente GenAI: {e}")
#     genai_client = None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process_info', methods=['POST'])
def process_info():
    data = request.json
    # if not genai_client:
    #     return jsonify({"error": "Cliente GenAI não inicializado"}), 500

    user = User(
        name=data.get('name'),
        age=data.get('age'),
        city=data.get('city'),
        state=data.get('state')
    )

    is_gestation = data.get('is_gestation')
    results = {}

    if is_gestation == 'sim':
        user.week_gestation = data.get('week_gestation')
        if not user.week_gestation:
            return jsonify({"error": "Semana de gestação é obrigatória."}), 400

        context_gestation = str(f'Olá meu nome é {user.name}, tenho {user.age} anos e estou grávida de {user.week_gestation} semanas.')
        results['gestation_info'] = CallAgent.get_gestation_tracking_info(context_gestation)

        context_health = f'Estou em {user.city}-{user.state}, me ajude com informações sobre pronto de socorro próximo e profissionais de saúde.'
        results['health_info'] = CallAgent.get_health_info(context_health)

        context_analysis = f"{results['gestation_info']} \n {results['health_info']}"
        results['refinement_info'] = CallAgent.get_analysis_care(context_analysis)

    elif is_gestation == 'nao':
        baby_name = data.get('baby_name')
        baby_age = data.get('baby_age')
        if not baby_name or not baby_age:
            return jsonify({"error": "Nome e idade do bebê são obrigatórios."}), 400

        baby = Baby(name=baby_name, age=baby_age)

        context_newborn = str(f'Olá meu nome é {user.name}, tenho {user.age} anos e sou mãe do(a) {baby.name} de {baby.age} ano(s).')
        results['newborn_info'] = CallAgent.get_newborn_care_info(context_newborn)

        context_development = f'A/O bebê {baby.name} de {baby.age} ano(s).'
        results['development_info'] = CallAgent.get_development_info(context_development)

        context_health = f'Estou em {user.city}-{user.state}, me ajude com informações sobre pronto de socorro próximo e profissionais de saúde.'
        results['health_info'] = CallAgent.get_health_info(context_health)

        context_analysis = f"{results['newborn_info']} \n {results['development_info']} \n {results['health_info']}"
        results['refinement_info'] = CallAgent.get_analysis_care(context_analysis)
    else:
        return jsonify({"error": "Status de gestação inválido."}), 400

    return jsonify(results)

if __name__ == '__main__':
    # Certifique-se de que o GOOGLE_API_KEY está configurado no seu ambiente
    if not GOOGLE_API_KEY:
        print("AVISO: A variável de ambiente GOOGLE_API_KEY não está configurada.")
        print("O aplicativo usará dados simulados para as chamadas ao CallAgent.")
    # else:
    #     print(f"GOOGLE_API_KEY encontrada.") # Não imprima a chave em produção

    app.run(debug=True, host='0.0.0.0', port=5005) # debug=True para desenvolvimento