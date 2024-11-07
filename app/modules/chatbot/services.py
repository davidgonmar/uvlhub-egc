from openai import OpenAI


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
        
#Esto es provisional, esta puest en el .env pero esta por ahora. Quien haga la otra parte que lo quite.
# Habria que hacerlo asi llamando a las variables de entorno en routes.py al hacer el POST -> client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

api_key = ""
client = OpenAI(api_key=api_key)

chatbot = ChatbotService(client)
create_new_chat(chatbot.client)
    