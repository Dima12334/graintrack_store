from graintrack_store.core.adapters.repositories.base import BaseRepository
from graintrack_store.users.models import User


class UserRepository(BaseRepository):
    model = User
