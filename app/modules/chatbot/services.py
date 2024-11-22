import openai
import os


class ChatbotService:
    def __init__(self, api_key, instructions):
        openai.api_key = api_key
        self.instructions = instructions

    def get_response(self, user_input, context):
        try:
            # Agregar el mensaje del usuario al contexto
            context.append({"role": "user", "content": user_input})

            # Llamar a la API de OpenAI
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=context
            )

            # Obtener la respuesta del asistente
            response = completion["choices"][0]["message"]["content"]

            # Agregar la respuesta al contexto (si quieres mantenerlo para más mensajes)
            context.append({"role": "assistant", "content": response})

            return response, context
        except Exception as e:
            return f"Error: {e}", context


