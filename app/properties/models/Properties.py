from datetime import date
from typing import Optional

from sqlalchemy import String, Date, Integer, Sequence
from sqlalchemy.orm import mapped_column, Mapped, relationship

from properties.models.PropertyStatuses import PropertyStatuses
from properties.models.PropertyTypes import PropertyTypes

from db import Base


class Properties:
    def __init__(self, address: str, type: PropertyTypes,
                 status: PropertyStatuses, purchase_date: date, price: int):
        self.address = address
        self.type = type
        self.status = status
        self.purchase_date = purchase_date
        self.price = price * 100

    def __repr__(self):
        return (f"Property(address={self.address}, "
                f"type={self.type.value}, "
                f"status={self.status.value}, "
                f"purchase_date={self.purchase_date}, "
                f"price={self.price})")

class Property(Base):
    __tablename__ = "properties"

    id: Mapped[Optional[int]] = mapped_column(Integer, Sequence("properties_id_seq", start=4), primary_key=True,
                                              autoincrement=True,)
    address: Mapped[str] = mapped_column(String(250),nullable=False)
    type: Mapped[str] = mapped_column(String(12),nullable=False)
    status: Mapped[str] = mapped_column(String(12),nullable=False)
    purchase_date: Mapped[date] = mapped_column(Date,nullable=False)
    price: Mapped[int] = mapped_column(Integer,nullable=False)
    child_maintenances = relationship("Maintenance", back_populates="property", cascade="all, delete-orphan")
    child_tenants = relationship("Tenant", back_populates="property", cascade="all, delete-orphan")

    def __repr__(self):
            return (f"<Property(address={self.address}, type={self.type}, "
                    f"status={self.status}, purchase_date={self.purchase_date}, "
                    f"price={self.price})>")