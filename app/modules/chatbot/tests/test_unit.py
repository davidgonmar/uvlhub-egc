import pytest
from app.modules.chatbot.services import ChatbotService
import os

@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        pass

    yield test_client

api_key = os.getenv("OPENAI_API_KEY")

instrucciones = """
        Eres un asistente diseñado para responder únicamente preguntas relacionadas con la WikiEGC (Evolución de la Gestión y Configuración), 
        de la Universidad de Sevilla, de InnoSoft y sobre el formato de archivo uvl.
        No respondas preguntas relacionadas con política, religión, u otros temas no relacionados con los temas mencionados anteriormente.
        Si alguien pregunta sobre otro tema, responde: 'Lo siento, solo atiendo preguntas sobre EGC y uvl.'
        En caso de preguntas en otro idioma distinto al español, responde: 'Lo siento, solo tengo soporte para conversaciones en español.'
        """

@pytest.fixture
def chatbot_service():
    return ChatbotService(api_key, instrucciones)


def test_service_succesful_response_chatbot(chatbot_service):
    msg = "Me puedes contar algo sobre EGC?"
    context = [
            {"role": "system", "content": chatbot_service.instructions}
        ]
    response, _ = chatbot_service.get_response(msg, context)

    assert response != None
    assert response != 'Lo siento, solo atiendo preguntas sobre EGC y uvl.'
    assert response != 'Lo siento, solo tengo soporte para conversaciones en español.'

def test_service_response_out_of_context(chatbot_service):
    msg = "Hablame de politica, religion o algun tema de actualidad"
    context = [
            {"role": "system", "content": chatbot_service.instructions}
        ]
    response, _ = chatbot_service.get_response(msg, context)

    assert response != None
    assert response == 'Lo siento, solo atiendo preguntas sobre EGC y uvl.'

def test_service_response_not_supported_language(chatbot_service):
    msg = "Hi Romeo! How are you today?"
    context = [
            {"role": "system", "content": chatbot_service.instructions}
        ]
    response, _ = chatbot_service.get_response(msg, context)

    assert response != None
    assert response == 'Lo siento, solo tengo soporte para conversaciones en español.'