from sqlalchemy import select, update

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DeliveryPartner


async def get_delivery_partner_user_id(
        db: AsyncSession,
        user_id: int,
    ):

    result = await db.execute(
        select(DeliveryPartner)
        .where(
            DeliveryPartner.user_id == user_id
        )
    )

    return result.scalar_one_or_none()


async def get_delivery_partner_by_id(
        db: AsyncSession,
        partner_id: int,
    ):

    result = await db.execute(
        select(DeliveryPartner)
        .where(
            DeliveryPartner.id == partner_id
        )
    )

    return result.scalar_one_or_none()



async def get_all_delivery_partners(
        db: AsyncSession,
    ):

    result = await db.execute(
        select(DeliveryPartner)
        .order_by(
            DeliveryPartner.created_at.desc()
        )
    )

    return result.scalars().all()
