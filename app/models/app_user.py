# app/models/user.py
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class AppUser(Base):
    __tablename__ = "app_user"

    user_id: Mapped[int] = mapped_column(primary_key=True)

    account_id: Mapped[int] = mapped_column(ForeignKey("account.account_id", ondelete="CASCADE"),nullable=False)

    user_email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_login_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()")

    account: Mapped["Account"] = relationship("Account", back_populates="users") #Account in starting with capital letter is a Python model class. 