from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    preferred_format: Mapped[str] = mapped_column(String(30), default="TEXT")
    learning_requirement: Mapped[str | None] = mapped_column(String(30), nullable=True)

    user = relationship("User", backref="profile", uselist=False)
