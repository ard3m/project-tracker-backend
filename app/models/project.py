# app/models/project.py
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class Project(Base):
    __tablename__ = "project"
    project_id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.account_id", ondelete="CASCADE"),nullable=False)
    project_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), server_default="True", nullable=False)
    address: Mapped[str] = mapped_column(String(320))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()", nullable=False)
    updated_by: Mapped[int] = mapped_column(ForeignKey("app_user.user_id", ondelete="RESTRICT"), nullable=False) #ondelete="RESTRICT" prevents deleting a referenced user if that user is still listed as updated_by on any project.

    updated_by_user: Mapped["AppUser"] = relationship("AppUser")
