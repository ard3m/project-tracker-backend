# app/models/account.py
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class Account(Base):
    __tablename__ = "account"
    account_id: Mapped[int] = mapped_column(primary_key=True)
    account_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    account_email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)

    users: Mapped[List["AppUser"]] = relationship("AppUser", back_populates="account", cascade="all, delete-orphan")
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="account", cascade="all, delete-orphan")
    audit_logs: Mapped[List["AuditLog"]] = relationship("AuditLogs", back_populates="account")