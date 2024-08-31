from typing import Dict, Any, List, Optional
from uuid import UUID
from graintrack_store.core.adapters.repositories.base import BaseRepository, ModelType


class BaseService:
    repository: BaseRepository

    def list(self, filters: Dict[str, Any] = None) -> List[ModelType]:
        return self.repository.list(filters=filters)

    def retrieve(self, uuid: UUID) -> Optional[ModelType]:
        return self.repository.retrieve_by_uuid(instance_uuid=uuid)
