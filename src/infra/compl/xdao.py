from datetime import datetime
from pydantic import BaseModel, UUID4

from domain.compl.models import Service


class XCompl(BaseModel):
    """Модель жалобы на сервис."""

    id: UUID4
    compl_on_id: UUID4
    services: Service
    author_id: UUID4
    complaints: str
    is_notified: bool = False
    is_resolved: bool = False
    created_at: datetime = datetime.now()
