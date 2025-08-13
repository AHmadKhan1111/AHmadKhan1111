from sqlalchemy import Column, Integer, String, Float, Text, DateTime, func

from .database import Base


class Bird(Base):
    __tablename__ = "birds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    species = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False, default=0.0)
    in_stock = Column(Integer, nullable=False, default=0)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )