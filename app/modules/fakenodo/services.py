from app.modules.fakenodo.repositories import FakenodoRepository
from core.services.BaseService import BaseService


class FakenodoService(BaseService):
    def __init__(self):
        super().__init__(FakenodoRepository())