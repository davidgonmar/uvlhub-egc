from app.modules.chatbot import chatbot_bp
from flask import render_template, request, jsonify
from app.modules.chatbot.services import ChatbotService  
import os


api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No se encontró la clave de API 'OPENAI_API_KEY' en el entorno.")

instrucciones = """
        Eres un asistente diseñado para responder únicamente preguntas relacionadas con la WikiEGC (Evolución de la Gestión y Configuración), 
        de la Universidad de Sevilla, de InnoSoft y sobre el formato de archivo uvl.
        No respondas preguntas relacionadas con política, religión, u otros temas no relacionados con los temas mencionados anteriormente.
        Si alguien pregunta sobre otro tema, responde: 'Lo siento, solo atiendo preguntas sobre EGC y uvl.'
        """

chatbot_service = ChatbotService(api_key, instrucciones)


@chatbot_bp.route('/chatbot', methods=['GET'])
def index():
    return render_template('chatbot/index.html')

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_input = data.get("message")

        if not user_input:
            return jsonify({"error": "No se ha proporcionado ningún mensaje"}), 400


        context = [
            {"role": "system", "content": chatbot_service.instructions}
        ]

        response, _ = chatbot_service.get_response(user_input, context)

        return jsonify({"response": response})

    except Exception as e:
        print(f"Error en el servidor: {e}")
        return jsonify({"error": "Ocurrió un error en el servidor."}), 500
