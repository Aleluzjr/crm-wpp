from flask import Flask, request, jsonify
import logging
import sys
import os
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

app = Flask(__name__)

# Configuração do log para exibir no Render
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Configuração da API do WhatsApp
TOKEN = os.getenv("WHATSAPP_API_TOKEN")  # Pega o token do .env
URL_API = os.getenv("WHATSAPP_API_URL")  # Pega a URL da API do .env
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Capturar dados do request
        if request.content_type == 'application/json':
            data = request.get_json()
        elif request.content_type == 'application/x-www-form-urlencoded':
            data = request.form.to_dict()
        else:
            logging.error(f"❌ Unsupported Media Type: {request.content_type}")
            return jsonify({"error": "Invalid content type"}), 415

        if not data:
            logging.error("❌ No data received")
            return jsonify({"error": "No data received"}), 400

        logging.info(f"📩 Webhook recebido: {data}")

        # Verifica se os dados contêm os campos necessários
        numero = data.get("number")
        mensagem = data.get("message")

        if not numero or not mensagem:
            logging.error("❌ Campos 'number' e 'message' são obrigatórios.")
            return jsonify({"error": "Campos 'number' e 'message' são obrigatórios"}), 400

        # Criar payload para envio da mensagem
        payload = {"number": numero, "body": mensagem}

        # Enviar mensagem via API
        response = requests.post(URL_API, headers=HEADERS, json=payload, verify=False, timeout=70)

        if response.status_code == 200:
            logging.info(f"✅ Mensagem enviada para {numero}: {mensagem}")
            return jsonify({"status": "sucesso", "detalhe": "Mensagem enviada"}), 200
        elif response.status_code == 504:
            logging.warning("⚠️ Erro 504 - A API pode ter enviado a mensagem mesmo assim.")
            return jsonify({"status": "aviso", "detalhe": "Erro 504 - A API pode ter enviado a mensagem"}), 504
        else:
            logging.error(f"❌ Falha ao enviar mensagem: {response.status_code} - {response.text}")
            return jsonify({"status": "erro", "codigo": response.status_code, "resposta": response.text}), response.status_code

    except requests.exceptions.RequestException as e:
        logging.error(f"🛑 Erro na requisição: {e}", exc_info=True)
        return jsonify({"error": "Erro ao enviar mensagem"}), 500

    except Exception as e:
        logging.error(f"⚠️ Erro inesperado: {e}", exc_info=True)
        return jsonify({"error": "Algo deu errado"}), 500

# 🚀 Rota de teste para validar se o webhook está online
@app.route('/webhook/test', methods=['GET'])
def webhook_test():
    logging.info("🔍 Teste de webhook realizado.")
    return jsonify({"status": "sucesso", "mensagem": "Webhook funcionando corretamente"}), 200

# 🏠 Rota principal para verificar se o servidor está rodando
@app.route('/', methods=['GET'])
def home():
    logging.info("🏠 Rota principal acessada.")
    return "Webhook server is running!", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
