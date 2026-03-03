# app/models/image.py
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class Image(Base):
    __tablename__ = "image"
    image_id: Mapped[int] = mapped_column(primary_key=True)
    file_path: Mapped[str] = mapped_column(String, nullable=False)  # TEXT path to file
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()", nullable=False)
    uploaded_by: Mapped[int] = mapped_column(ForeignKey("app_user.user_id", ondelete="RESTRICT"), nullable=False)

    uploaded_by_user: Mapped["AppUser"] = relationship("AppUser")