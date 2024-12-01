from app.modules.fakenodo.models import Fakenodo
from core.repositories.BaseRepository import BaseRepository


class FakenodoRepository(BaseRepository):
    def __init__(self):
        # Initialize the base repository, not FakenodoRepository itself
        super().__init__(Fakenodo)