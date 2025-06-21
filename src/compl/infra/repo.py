from uuid import UUID
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, func

from ..domain.irepo import IComplRepo
from ..domain.dto import Service, QCreateCompl, QFilter
from ..domain.models import Complaints

from .xdao import XCompl


class ComplRepo(IComplRepo):
    """Реализация репозитория для работы с жалобами.

    Args:
        _session (AsyncSession): Асинхронная сессия базы данных.
    """

    def __init__(self, _session: AsyncSession):
        self.session: AsyncSession = _session

    async def create_compl(self, req: QCreateCompl) -> XCompl:
        """Создаёт новую жалобу в базе данных.

        Args:
            req (QCreateCompl): Данные для создания жалобы.

        Returns:
            XCompl: Созданный объект жалобы.
        """
        req = (
            insert(Complaints)
            .values(
                compl_on_id=req.compl_on_id,
                services=req.service.value,
                author_id=req.author_id,
                complaints=req.complaints,
                is_notified=req.is_notified,
                is_resolved=req.is_resolved,
            )
            .returning(Complaints)
        )
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one()
        return XCompl(
            id=row.id,
            compl_on_id=row.compl_on_id,
            services=row.services,
            author_id=row.author_id,
            complaints=row.complaints,
            is_notified=row.is_notified,
            is_resolved=row.is_resolved,
            created_at=row.created_at,
        )

    async def get_my_complaint(self, compl_id: UUID, acc_id: UUID) -> XCompl:
        """Получает жалобу пользователя по ID.

        Args:
            compl_id (UUID): ID жалобы.
            acc_id (UUID): ID автора жалобы.

        Returns:
            XCompl: Найденная жалоба.

        Raises:
            KeyError: Если жалоба не найдена.
        """
        req = select(Complaints).where(
            Complaints.id == compl_id, Complaints.author_id == acc_id
        )
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one_or_none()
        if not row:
            raise KeyError("Жалоба в бд не найдена")

        return XCompl(
            id=row.id,
            compl_on_id=row.compl_on_id,
            services=row.services,
            author_id=row.author_id,
            complaints=row.complaints,
            is_notified=row.is_notified,
            is_resolved=row.is_resolved,
            created_at=row.created_at,
        )

    async def get_my_complaints(
        self, acc_id: UUID, complaints_of: Service | None = None
    ) -> list[XCompl]:
        """Получает список жалоб пользователя, с подсчётом по типам.

        Args:
            acc_id (UUID): ID автора жалоб.
            complaints_of (Service | None, optional): Фильтр по типу сервиса. По умолчанию None.

        Returns:
            tuple[int, int, list[XCompl]]: Количество жалоб на аккаунт, количество жалоб на объявления и список жалоб.
        """
        count_compl_acc = (
            select(func.count())
            .select_from(Complaints)
            .where(
                Complaints.services == Service.ACCOUNT.value,
                Complaints.author_id == acc_id,
            )
        )
        count_res = await self.session.execute(count_compl_acc)
        await self.session.commit()
        total_acc = count_res.scalar_one()

        count_compl_ads = (
            select(func.count())
            .select_from(Complaints)
            .where(
                Complaints.services == Service.ADS.value, Complaints.author_id == acc_id
            )
        )
        count_res = await self.session.execute(count_compl_ads)
        await self.session.commit()
        total_ads = count_res.scalar_one()

        if complaints_of is Service.ACCOUNT:
            compl_acc_req = select(Complaints).where(
                Complaints.services == complaints_of.value,
                Complaints.author_id == acc_id,
            )
            xres_acc = await self.session.execute(compl_acc_req)
            await self.session.commit()
            res = []
            for row in xres_acc.scalars().all():
                res.append(
                    XCompl(
                        id=row.id,
                        compl_on_id=row.compl_on_id,
                        services=row.services,
                        author_id=row.author_id,
                        complaints=row.complaints,
                        is_notified=row.is_notified,
                        is_resolved=row.is_resolved,
                        created_at=row.created_at,
                    )
                )

        elif complaints_of is Service.ADS:
            compl_ads_req = select(Complaints).where(
                Complaints.services == complaints_of.value,
                Complaints.author_id == acc_id,
            )
            xres_ads = await self.session.execute(compl_ads_req)
            await self.session.commit()
            res = []
            for row in xres_ads.scalars().all():
                res.append(
                    XCompl(
                        id=row.id,
                        compl_on_id=row.compl_on_id,
                        services=row.services,
                        author_id=row.author_id,
                        complaints=row.complaints,
                        is_notified=row.is_notified,
                        is_resolved=row.is_resolved,
                        created_at=row.created_at,
                    )
                )

        else:
            req = select(Complaints).where(Complaints.author_id == acc_id)
            xres = await self.session.execute(req)
            await self.session.commit()
            res = []
            for row in xres.scalars().all():
                res.append(
                    XCompl(
                        id=row.id,
                        compl_on_id=row.compl_on_id,
                        services=row.services,
                        author_id=row.author_id,
                        complaints=row.complaints,
                        is_notified=row.is_notified,
                        is_resolved=row.is_resolved,
                        created_at=row.created_at,
                    )
                )
        return total_acc, total_ads, res

    async def adm_get_complaint(self, compl_id: UUID) -> XCompl:
        """Получает жалобу по ID для администратора.

        Args:
            compl_id (UUID): ID жалобы.

        Returns:
            XCompl: Найденная жалоба.

        Raises:
            KeyError: Если жалоба не найдена.
        """
        req = select(Complaints).where(Complaints.id == compl_id)
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one_or_none()
        if not row:
            raise KeyError("Жалоба в бд не найдена")

        return XCompl(
            id=row.id,
            compl_on_id=row.compl_on_id,
            services=row.services,
            author_id=row.author_id,
            complaints=row.complaints,
            is_notified=row.is_notified,
            is_resolved=row.is_resolved,
            created_at=row.created_at,
        )

    async def adm_get_complaints(self, qfilter: QFilter) -> list[XCompl]:
        """Получает список жалоб для администратора с фильтрацией и подсчётом.

        Args:
            qfilter (QFilter): Параметры фильтрации и пагинации.

        Returns:
            tuple[int, int, list[XCompl]]: Количество жалоб на аккаунт, количество жалоб на объявления и список жалоб.
        """
        count_compl_acc = (
            select(func.count())
            .select_from(Complaints)
            .where(Complaints.services == Service.ACCOUNT.value)
        )
        count_res = await self.session.execute(count_compl_acc)
        await self.session.commit()
        total_acc = count_res.scalar_one()

        count_compl_ads = (
            select(func.count())
            .select_from(Complaints)
            .where(Complaints.services == Service.ADS.value)
        )
        count_res = await self.session.execute(count_compl_ads)
        await self.session.commit()
        total_ads = count_res.scalar_one()

        req = select(Complaints).limit(qfilter.limit).offset(qfilter.offset)

        if qfilter.complaints_of:
            req = req.where(Complaints.services == qfilter.complaints_of.value)

        if qfilter.is_today:
            today = date.today()
            tomorrow = today + timedelta(days=1)

            req = req.where(Complaints.created_at.between(today, tomorrow))

        if qfilter.is_notified:
            req = req.where(Complaints.is_notified == qfilter.is_notified)

        if qfilter.is_resolved:
            req = req.where(Complaints.is_resolved == qfilter.is_resolved)

        xres = await self.session.execute(req)
        await self.session.commit()
        res = []
        for row in xres.scalars().all():
            res.append(
                XCompl(
                    id=row.id,
                    compl_on_id=row.compl_on_id,
                    services=row.services,
                    author_id=row.author_id,
                    complaints=row.complaints,
                    is_notified=row.is_notified,
                    is_resolved=row.is_resolved,
                    created_at=row.created_at,
                )
            )

        return total_acc, total_ads, res
