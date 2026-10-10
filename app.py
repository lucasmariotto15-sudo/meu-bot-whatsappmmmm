import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
Você é a atendente virtual de uma loja de imagens personalizadas por Inteligência Artificial chamada "Arte Mágica".
Seu objetivo é guiar o cliente de forma simpática, curta e vendedora pelo seguinte funil no WhatsApp:
1. Saudação e apresentação dos temas disponíveis (Ex: 1. Abraçado com Jesus, 2. Guerreiro Épico).
2. Após o cliente escolher o tema, pedir para ele enviar uma foto de boa qualidade e bem iluminada.
3. Informar que após o envio da foto, o valor é R$ 19,90 e gerar o Pix.
Mantenha as respostas curtas, ideais para o formato de mensagens de WhatsApp, usando emojis.
"""

@app.route("/", methods=["GET"])
def home():
    return "Bot do WhatsApp com Gemini rodando com sucesso!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"status": "ignored"}), 200

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_message,
        config={
            "system_instruction": SYSTEM_PROMPT,
        },
    )
    
    bot_reply = response.text
    return jsonify({"status": "success", "reply": bot_reply}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
