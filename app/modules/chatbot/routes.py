from flask import render_template
from app.modules.chatbot import chatbot_bp
from flask import Blueprint, render_template, request, jsonify
from openai import OpenAI
import os



@chatbot_bp.route('/chatbot', methods=['GET'])
def index():
    return render_template('chatbot/index.html')

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def get_chat_response(user_input):
    messages = [
        {"role": "system", "content": "Eres un chatbot"}
    ]
    messages.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return completion.choices[0].message.content

# Ruta API para manejar los mensajes del usuario y responder
@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    try:
        # Obtén el mensaje JSON del cliente
        data = request.json
        user_input = data.get("message")

        # Verifica que el mensaje no esté vacío
        if not user_input:
            return jsonify({"error": "No se ha proporcionado ningún mensaje"}), 400

        # Intenta obtener la respuesta del chatbot
        response = get_chat_response(user_input)
        return jsonify({"response": response})


    except Exception as e:
        # Maneja cualquier otro error
        print(f"Error en el servidor: {e}")
        return jsonify({"error": "Ocurrió un error en el servidor."}), 500
