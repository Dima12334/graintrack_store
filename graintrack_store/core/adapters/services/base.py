from typing import Dict, Any, List, Optional
from uuid import UUID
from graintrack_store.core.adapters.repositories.base import BaseRepository, ModelType
from graintrack_store.users.models import User


class BaseService:
    repository: BaseRepository

    def list(self, user: User, filters: Dict[str, Any] = None) -> List[ModelType]:
        return self.repository.list(filters=filters)

    def retrieve(self, uuid: UUID) -> Optional[ModelType]:
        return self.repository.retrieve_by_uuid(instance_uuid=uuid)
