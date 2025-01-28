from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configuração do arquivo de log
logging.basicConfig(
    filename='webhook.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Token para autenticação (exemplo)
AUTH_TOKEN = 'SOME-VALUE'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    try:
        # Verificar se a requisição contém o cabeçalho Authorization com o token correto
        token = request.headers.get('Authorization')
        if not token or token != f'Bearer {AUTH_TOKEN}':
            return jsonify({"error": "Unauthorized"}), 401

        # Validação do método da requisição
        if request.method == 'GET':
            # Resposta para validação da URL pela plataforma
            return jsonify({"message": "Webhook is live!"}), 200

        elif request.method == 'POST':
            # Receber os dados no formato JSON
            data = request.get_json()
            if not data:
                return jsonify({"error": "No JSON received"}), 400

            # Registrar os dados no arquivo de log
            logging.info(f"Received data: {data}")
            return jsonify({"message": "Data received successfully"}), 200

    except Exception as e:
        # Captura erros e registra no log
        logging.error(f"Error: {e}")
        return jsonify({"error": "Something went wrong"}), 500
    
# Rota para verificar se o servidor está funcionando
@app.route('/', methods=['GET'])
def home():
    return "Webhook server is running!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
