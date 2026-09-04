from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    DECIMAL,
    ForeignKey
)
from decimal import Decimal

from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.core import OrderStatus
from sqlalchemy import Enum

from datetime import datetime

from app.db import Base

if TYPE_CHECKING:
    from order import Order


class OrderTracking(Base):

    __tablename__ = "order_tracking"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
        index=True
    )

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False,
        index=True
    )

    latitude: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 7),
        nullable=True
    )

    longitude: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 7),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # RELATIONSHIPS

    order: Mapped["Order"] = relationship(
        back_populates="tracking_updates"
    )