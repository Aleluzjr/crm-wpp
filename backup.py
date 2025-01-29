from flask import Flask, request, jsonify
import logging
import sys
import os

app = Flask(__name__)

# Configuração do arquivo de log para a saída padrão (stdout)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    try:
        # Verificar se o Content-Type é application/json
        if request.content_type == 'application/json':
            data = request.get_json()
        elif request.content_type == 'application/x-www-form-urlencoded':
            # Quando o tipo for 'application/x-www-form-urlencoded', processa os dados
            data = request.form.to_dict()
        else:
            logging.error(f"Unsupported Media Type: {request.content_type}")
            return jsonify({"error": "Invalid content type, expected application/json or application/x-www-form-urlencoded"}), 415

        # Se não houver dados, retorna erro
        if not data:
            logging.error("No data received")
            return jsonify({"error": "No data received"}), 400

        # Registrar os dados no arquivo de log
        logging.info(f"Received data: {data}")
        return jsonify({"message": "Data received successfully"}), 200

    except Exception as e:
        # Captura erros e registra no log
        logging.error(f"Exception occurred: {str(e)}", exc_info=True)
        return jsonify({"error": "Something went wrong"}), 500
    
# Rota para verificar se o servidor está funcionando
@app.route('/', methods=['GET'])
def home():
    logging.info("Home route accessed.")
    return "Webhook server is running!", 200

if __name__ == '__main__':
    # Obter a porta do ambiente (Render define a variável PORT)
    port = int(os.environ.get("PORT", 5000))
    # Inicia o servidor Flask na porta correta
    app.run(host='0.0.0.0', port=port)