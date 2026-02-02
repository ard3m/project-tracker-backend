from datetime import datetime
from app.repositories.history_repository import HistoryRepository
from app.schemas.history import HistoryEventOut


class HistoryService:
    def __init__(self, repo: HistoryRepository):
        self.repo = repo

    def list_history(self):
        return self.repo.list_history()

    def record_event(self, event_type: str, description: str) -> HistoryEventOut:
        event = HistoryEventOut(
            history_event_id=self.repo.next_id,
            event_type=event_type,
            description=description,
            timestamp=datetime.utcnow()
        )

        self.repo.next_id += 1
        return self.repo.create_event(event)
