from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configuração do arquivo de log
logging.basicConfig(
    filename='webhook.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Receber os dados no formato JSON
        data = request.json
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        # Registrar os dados no arquivo de log
        logging.info(f"Received data: {data}")
        return jsonify({"message": "Data received successfully"}), 200

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": "Something went wrong"}), 500

# Rota para verificar se o servidor está funcionando
@app.route('/', methods=['GET'])
def home():
    return "Webhook server is running!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
