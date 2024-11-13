from openai import OpenAI
import os


class ChatbotService():

    def __init__(self, client):
        self.client = client

def create_new_chat(client):
        messages = [
            {"role": "system", "content": "Eres un chatbot"}
        ]
        while True:
            prompt = input("Tu: ")
            #Esto es para salir de la conversacion desde la terminal, habría que retocar
            if prompt.lower() == "salir":
                break
            messages.append({"role": "user", "content": prompt})

            completion = client.chat.completions.create(
                model="gpt-4o",
                messages = messages
            )

            response = completion.choices[0].message.content
            print(f"Romeo: {response}")

        

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

chatbot = ChatbotService(client)
create_new_chat(chatbot.client)
    