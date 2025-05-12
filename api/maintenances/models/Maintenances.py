from datetime import date
from typing import Optional
from db import Base
from sqlalchemy import String, Integer, ForeignKey, Sequence, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from maintenances.models.MaintenanceStatuses import MaintenanceStatuses




class Maintenances():
    def __init__(self, task_description: str, status: MaintenanceStatuses, scheduled_date: date, property_id:int):
        self.task_description = task_description
        self.status = status
        self.scheduled_date = scheduled_date
        self.property_id = property_id

        def __repr__(self):
            return (f"Maintenances(task_description='{self.task_description}', status='{self.status}', "
                    f"scheduled_date='{self.scheduled_date}')")

class Maintenance(Base):
    __tablename__ = "maintenances"
    id: Optional[int] = mapped_column(Integer, Sequence("maintenances_id_seq", start=4), primary_key=True,
                                              autoincrement=True)
    task_description = mapped_column(String(250), nullable=False)
    status = mapped_column(String(11), nullable=False)
    scheduled_date = mapped_column(Date, nullable=False)
    property_id = mapped_column(ForeignKey("kata_python.properties.id", ondelete='CASCADE'))
    property = relationship("Property", back_populates="child_maintenances")

    def __repr__(self):
        return (f"<Maintenance(task_description={self.task_description}, "
                f"status={self.status}, "
                f"scheduled_date={self.scheduled_date}, "
                f"property_id={self.property_id})>")
