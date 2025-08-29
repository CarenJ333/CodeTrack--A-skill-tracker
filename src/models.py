from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from .db import Base
from sqlalchemy.orm import relationship

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # One Skill -> Many CodingSessions
    sessions = relationship("CodingSession", back_populates="skill")

    def __repr__(self):
        return f"<Skill {self.id}: {self.name}>"

class CodingSession(Base):
    __tablename__ = "coding_sessions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)  # auto timestamp
    duration = Column(Integer, nullable=False)        # in minutes
    language = Column(String, nullable=False)
    notes = Column(String, nullable=True)

    # Foreign key linking to Skill
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)

    # Relationship back to Skill
    skill = relationship("Skill", back_populates="sessions")

    def __repr__(self):
        return f"<Session {self.id}: {self.language} ({self.skill.name}) - {self.duration}min>"
