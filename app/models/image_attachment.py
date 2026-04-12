# app/models/imageattachment.py
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

class ImageAttachment(Base):
    __tablename__ = "image_attachment"
    image_attachment_id: Mapped[int] = mapped_column(primary_key=True)
    image_id: Mapped[int] = mapped_column(ForeignKey("image.image_id", ondelete="CASCADE"), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False) #for example: 'project', 'task', 'project_access', ect.
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False) #this is taken from the PRIMARY KEY of the above entity_type (project/task/ect)
    #the entity_type and entity_id are kind of like foreign keys - but also not really
        #I've looked it up, they are called 'logical foreign keys', not 'database-enforced foreign keys'.

    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()", nullable=False)
    uploaded_by: Mapped[int] = mapped_column(ForeignKey("app_user.user_id", ondelete="RESTRICT"), nullable=False)

    uploaded_by_user: Mapped["AppUser"] = relationship("AppUser")
    image: Mapped["Image"] = relationship("Image")