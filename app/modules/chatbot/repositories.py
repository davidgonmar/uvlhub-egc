from app.modules.chatbot.models import Chatbot
from core.repositories.BaseRepository import BaseRepository


class ChatbotRepository(BaseRepository):
    def __init__(self):
        super().__init__(Chatbot)
