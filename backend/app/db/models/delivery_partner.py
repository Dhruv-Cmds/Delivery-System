from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    DECIMAL,
    ForeignKey
)

from decimal import Decimal

from app.core import DeliveryPartnerStatus
from sqlalchemy import Enum

from sqlalchemy.orm import relationship, mapped_column, Mapped

from datetime import datetime

from app.core import VehicleTypeStatus
from sqlalchemy import Enum

from app.db import Base

if TYPE_CHECKING:
    from order import Order
    from user import User


class DeliveryPartner(Base):

    __tablename__ = "delivery_partners"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True
    )

    vehicle_type: Mapped[VehicleTypeStatus] = mapped_column(
        Enum(VehicleTypeStatus),
        nullable=False
    )

    status: Mapped[DeliveryPartnerStatus] = mapped_column(
        Enum(DeliveryPartnerStatus),
        default=DeliveryPartnerStatus.AVAILABLE,
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

    rating: Mapped[Decimal] = mapped_column(
        DECIMAL(2, 1),
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

    user: Mapped["User"] = relationship(
        back_populates="delivery_partner"
    )

    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="delivery_partner"
    )