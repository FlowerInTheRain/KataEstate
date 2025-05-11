from datetime import date
from typing import Optional

from sqlalchemy import String, Integer, Date, ForeignKey, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

from properties.models.PaymentStatuses import PaymentStatuses


class Tenants:
    def __init__(self, name: str,
                 contact_info: str,
                 lease_term_start: Date,
                 lease_term_end: Date,
                 rent_paid: PaymentStatuses):
        self.name = name
        self.contact_info = contact_info
        self.lease_term_start = lease_term_start
        self.lease_term_end = lease_term_end
        self.rent_paid = rent_paid

    def __repr__(self):
        status = "Paid" if self.rent_paid else "Unpaid"
        return (f"Tenant(name='{self.name}', contact='{self.contact_info}', "
                f"lease_term_start='{self.lease_term_start}'"
                f"lease_term_end='{self.lease_term_end}', "
                f", rent_status='{status}')")

class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[Optional[int]] = mapped_column(Integer, Sequence("tenants_id_seq", start=4), primary_key=True,
                                              autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    contact_info: Mapped[str] = mapped_column(String(100), nullable=False)
    lease_term_start: Mapped[date] = mapped_column(Date, nullable=False)
    lease_term_end: Mapped[date] = mapped_column(Date, nullable=False)
    rent_paid: Mapped[str] = mapped_column(String(10), nullable=False)
    property_id = mapped_column(ForeignKey("kata_python.properties.id"))
    property = relationship("Property", back_populates="child_tenants")

    def __repr__(self):
            return (f"<Tenant(name={self.name}, contact_info={self.contact_info}, "
                    f"lease_term_start={self.lease_term_start},lease_term_end={self.lease_term_end}, rent_paid"
                    f"={self.rent_paid}, "
                    f"property_id={self.property_id})>")