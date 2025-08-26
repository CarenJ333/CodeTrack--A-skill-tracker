from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .db import Base

class CodingSession(Base):
    __tablename__ = "coding_sessions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)  # auto timestamp
    duration = Column(Integer, nullable=False)        # in minutes
    language = Column(String, nullable=False)
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<Session {self.id}: {self.language} - {self.duration}min>"
