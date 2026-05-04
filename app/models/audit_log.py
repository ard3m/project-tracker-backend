# app/models/auditlog.py
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class AuditLog(Base):
    __tablename__ = "audit_log"
    audit_id: Mapped[int] = mapped_column(primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False) #for example: 'project', 'task', 'project_access', ect.
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False) #this is taken from the PRIMARY KEY of the above entity_type (project/task/ect)
    #the entity_type and entity_id are kind of like foreign keys - but also not really
        #I've looked it up, they are called 'logical foreign keys', not 'database-enforced foreign keys'.
    account_id: Mapped[int] = mapped_column(ForeignKey("account.account_id", ondelete="RESTRICT"),nullable=False) #must be RESTRICT
    performed_by: Mapped[int] = mapped_column(ForeignKey("app_user.user_id", ondelete="RESTRICT"), nullable=False)
    performed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    details: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    account = relationship("Account", lazy="joined")
    user = relationship("AppUser", lazy="joined")