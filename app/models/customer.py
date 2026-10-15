from datetime import UTC, datetime

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import UTCDateTime
from app.domain.customer import CustomerStatus


def utc_now() -> datetime:
    return datetime.now(UTC)


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = (
        UniqueConstraint("email", name="uq_customers_email"),
        Index("ix_customers_email", "email"),
        Index("ix_customers_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    status: Mapped[CustomerStatus] = mapped_column(
        SQLAlchemyEnum(
            CustomerStatus,
            name="customer_status",
            native_enum=False,
            create_constraint=True,
            length=16,
            values_callable=lambda enum: [member.value for member in enum],
        ),
        nullable=False,
        default=CustomerStatus.PENDING,
    )
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        nullable=False,
        default=utc_now,
    )
