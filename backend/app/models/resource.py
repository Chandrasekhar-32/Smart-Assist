from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    type: Mapped[str] = mapped_column(String(30))  # TEXT | SIMPLIFIED_TEXT | VISUAL | AUDIO | SHORT_LESSON
    title: Mapped[str] = mapped_column(String(160))
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    media_url: Mapped[str | None] = mapped_column(String(400), nullable=True)

    lesson = relationship("Lesson", back_populates="resources")
