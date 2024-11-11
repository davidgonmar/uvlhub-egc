from flask import render_template
from app.modules.chatbot import chatbot_bp
from flask import Blueprint, render_template, request, jsonify
from openai import OpenAI
import os



@chatbot_bp.route('/chatbot', methods=['GET'])
def index():
    return render_template('chatbot/index.html')


def get_chat_response(user_input):
    messages = [
        {"role": "system", "content": "Eres un chatbot"}
    ]
    messages.append({"role": "user", "content": user_input})

    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return completion.choices[0].message.content

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_input = data.get("message")

        if not user_input:
            return jsonify({"error": "No se ha proporcionado ningún mensaje"}), 400

        response = get_chat_response(user_input)
        return jsonify({"response": response})


    except Exception as e:
        print(f"Error en el servidor: {e}")
        return jsonify({"error": "Ocurrió un error en el servidor."}), 500
