# app/models/task.py
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class Task(Base):
    __tablename__ = "task"
    task_id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.project_id", ondelete="CASCADE"), nullable=False) #foreign key
    task_name: Mapped[str] = mapped_column(String(30), nullable=False)
    task_details: Mapped[str] = mapped_column(String) #TEXT, changed from task_description
    is_active: Mapped[bool] = mapped_column(Boolean(), server_default="true", nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()", nullable=False)
    updated_by: Mapped[int] = mapped_column(ForeignKey("app_user.user_id", ondelete="RESTRICT"), nullable=False) #ondelete="RESTRICT" prevents deleting a referenced user if that user is still listed as updated_by on any project.

    updated_by_user: Mapped["AppUser"] = relationship("AppUser")