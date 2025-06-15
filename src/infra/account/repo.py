from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete, update, text
from sqlalchemy.exc import NoResultFound

from domain.account.irepo import IAccRepo
from domain.account.models import Account, AccRole
from domain.account.dto import QEmailSignupData, BannedTo

from .xdao import XAccount, XAccountID


class AccRepo(IAccRepo):
    """Реализация репозитория для работы с пользовательскими аккаунтами через AsyncSession."""

    def __init__(self, _session: AsyncSession):
        """Инициализирует репозиторий с сессией базы данных.

        Args:
            _session (AsyncSession): Асинхронная сессия работы с базой данных.
        """

        self.session: AsyncSession = _session

    async def get_account_by_id(self, count_ads: int, acc_id: UUID) -> XAccount:
        """Получает аккаунт по его ID.

        Args:
            acc_id (UUID): Уникальный идентификатор аккаунта.

        Returns:
            XAccount: Объект аккаунта.

        Raises:
            KeyError: Если аккаунт не найден.
        """
        update_ads_req = (
            update(Account)
            .values(count_ads=count_ads)
            .where(Account.id==acc_id)
        )
        await self.session.execute(update_ads_req)
        await self.session.commit()

        req = select(Account).where(Account.id == acc_id)
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one_or_none()
        if row is None:
            raise KeyError("Отсутствует запись об аккаунте")
        return XAccount(
            id=row.id,
            email=row.email,
            pwd_hash=row.pwd_hash,
            salt=row.salt,
            role=row.role,
            count_ads=row.count_ads,
            is_banned=row.is_banned,
            created_at=row.created_at,
            updated_at=row.updated_at,
            blocked_at=row.blocked_at,
            reason_blocked=row.reason_blocked,
            blocked_to=row.blocked_to,
        )

    async def get_account_by_email(self, email: str, count_ads: int | None = None) -> XAccount:
        """Получает аккаунт по email.

        Args:
            email (str): Электронная почта пользователя.

        Returns:
            XAccount: Объект аккаунта.

        Raises:
            KeyError: Если аккаунт не найден.
        """
        if count_ads:
            update_ads_req = (
                update(Account)
                .values(count_ads=count_ads)
                .where(Account.email==email)
            )
            await self.session.execute(update_ads_req)
            await self.session.commit()

        req = select(Account).where(Account.email == email)
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one_or_none()
        if row is None:
            raise KeyError("Отсутствует запись об аккаунте")
        return XAccount(
            id=row.id,
            email=row.email,
            pwd_hash=row.pwd_hash,
            salt=row.salt,
            role=row.role,
            count_ads=row.count_ads,
            is_banned=row.is_banned,
            created_at=row.created_at,
            updated_at=row.updated_at,
            blocked_at=row.blocked_at,
            reason_blocked=row.reason_blocked,
            blocked_to=row.blocked_to,
        )

    async def copy_account_from_signup(self, x_signup: QEmailSignupData) -> XAccountID:
        """Копирует данные из временной регистрации в аккаунт.

        Args:
            x_signup (QEmailSignupData): Данные временной регистрации.

        Returns:
            XAccountID: Идентификатор созданного аккаунта.
        """
        req = (
            insert(Account)
            .values(
                email=x_signup.email,
                pwd_hash=x_signup.pwd_hash,
                salt=x_signup.salt,
                role=AccRole.USER.value,
            )
            .returning(Account)
        )
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one()
        return XAccountID(id=row.id)

    async def is_email_busy(self, email: str) -> bool:
        """Проверяет, занят ли email.

        Args:
            email (str): Электронная почта для проверки.

        Returns:
            bool: True, если email занят, иначе False.
        """
        req = select(Account).where(Account.email == email)
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one_or_none()
        return row is not None

    async def get_accounts(self) -> list[XAccount]:
        """Возвращает список всех аккаунтов (до 10 штук).

        Returns:
            list[XAccount]: Список аккаунтов.
        """
        req = select(Account).limit(10)
        xres = await self.session.execute(req)
        await self.session.commit()
        res = []
        for row in xres.scalars().all():
            res.append(
                XAccount(
                    id=row.id,
                    email=row.email,
                    pwd_hash=row.pwd_hash,
                    salt=row.salt,
                    role=row.role,
                    count_ads=row.count_ads,
                    is_banned=row.is_banned,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                    blocked_at=row.blocked_at,
                    reason_blocked=row.reason_blocked,
                    blocked_to=row.blocked_to,
                )
            )
        return res

    async def get_current_account(self, count_ads: int, acc_id: UUID) -> XAccount:
        update_ads_req = (
            update(Account)
            .values(count_ads=count_ads)
            .where(Account.id==acc_id)
        )
        await self.session.execute(update_ads_req)
        await self.session.commit()

        req = select(Account).where(Account.id == acc_id)
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one()

        return XAccount(
            id=row.id,
            email=row.email,
            pwd_hash=row.pwd_hash,
            salt=row.salt,
            role=row.role,
            count_ads=row.count_ads,
            is_banned=row.is_banned,
            created_at=row.created_at,
            updated_at=row.updated_at,
            blocked_at=row.blocked_at,
            reason_blocked=row.reason_blocked,
            blocked_to=row.blocked_to,
        )

    async def delete_acc(self, acc_id: UUID) -> None:
        """Удаляет аккаунт по ID.

        Args:
            acc_id (UUID): Уникальный идентификатор аккаунта.

        Returns:
            None
        """
        req = delete(Account).where(Account.id == acc_id)
        await self.session.execute(req)
        await self.session.commit()

    async def set_role_account(self, acc_id: UUID, role: AccRole) -> None:
        req = (
            update(Account)
            .values(role=role.value)
            .where(Account.id == acc_id)
        )
        try:
            await self.session.execute(req)
        except NoResultFound as e:
            raise KeyError("Аккаунт в бд не найден") from e
        await self.session.commit()

    async def set_ban_account(self, acc_id: UUID, blocked_to: BannedTo, reason_banned: str) -> str:
        blocked_mapping = {
            "week": text("NOW() + INTERVAL '7 DAYS'"),
            "month": text("NOW() + INTERVAL '1 MONTH'"),
            "month3": text("NOW() + INTERVAL '3 MONTHS'"),
            "year": text("NOW() + INTERVAL '1 YEAR'"),
            "forever": text("'infinity'::timestamp"),
        }

        ban_time = blocked_mapping.get(blocked_to.value)

        req = (
            update(Account)
            .values(
                is_banned=True,
                blocked_at=text("NOW()"),
                reason_blocked=reason_banned,
                blocked_to=ban_time,
            )
            .where(Account.id == acc_id)
            .returning(Account)
        )
        try:
            res = await self.session.execute(req)
        except NoResultFound as e:
            raise KeyError("Аккаунт в бд не найден") from e
        await self.session.commit()

        row = res.scalar_one()
        return str(row.blocked_to)


    async def set_unban_account(self, acc_id: UUID) -> None:
        req = (
            update(Account)
            .values(
                is_banned=False,
                blocked_at=None,
                reason_blocked=None,
                blocked_to=None,
            )
            .where(Account.id == acc_id)
        )
        try:
            await self.session.execute(req)
        except NoResultFound as e:
            raise KeyError("Аккаунт в бд не найден") from e
        await self.session.commit()
