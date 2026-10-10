from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[str] = mapped_column(String(20), default="EASY")  # EASY | MEDIUM | HARD
    position: Mapped[int] = mapped_column(Integer, default=0)

    subject = relationship("Subject", back_populates="lessons")
    resources = relationship("Resource", back_populates="lesson")
    quiz = relationship("Quiz", back_populates="lesson", uselist=False)
