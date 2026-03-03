# app/models/contacts.py
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class Contacts(Base):
    __tablename__ = "project_contacts"
    project_id: Mapped[int] = mapped_column(ForeignKey("project.project_id", ondelete="CASCADE"), primary_key=True)
    project_contacts_details: Mapped[str] = mapped_column(String) #TEXT, changed from  project_contact_notes
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()", nullable=False)
    updated_by: Mapped[int] = mapped_column(ForeignKey("app_user.user_id", ondelete="RESTRICT"), nullable=False)

    updated_by_user: Mapped["AppUser"] = relationship("AppUser")