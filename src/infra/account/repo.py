from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete, update, text

from domain.account.irepo import IAccRepo
from domain.account.models import Account, AccRole
from domain.account.dto import QEmailSignupData

from .xdao import XAccount, XAccountID

class AccRepo(IAccRepo):

    def __init__(self, _session: AsyncSession):
        self.session: AsyncSession = _session

    async def get_account_by_id(self, acc_id: UUID) -> XAccount:
        req = (
            select(Account)
            .where(Account.id == acc_id)
        )
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
            is_banned=row.is_banned,
            created_at=row.created_at,
            updated_at=row.updated_at,
            blocked_at=row.blocked_at,
            blocked_till=row.blocked_till,
        )

    async def get_account_by_email(self, email: str) -> XAccount:
        req = (
            select(Account)
            .where(Account.email == email)
        )
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
            is_banned=row.is_banned,
            created_at=row.created_at,
            updated_at=row.updated_at,
            blocked_at=row.blocked_at,
            blocked_till=row.blocked_till,
        )

    async def copy_account_from_signup(self, x_signup: QEmailSignupData) -> XAccountID:
        req = (
            insert(Account)
            .values(
                email=x_signup.email,
                pwd_hash=x_signup.pwd_hash,
                salt=x_signup.salt,
                role=AccRole.USER.value
            )
            .returning(Account)
        )
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one()
        return XAccountID(id=row.id)

    async def is_email_busy(self, email: str) -> bool:
        req = (
            select(Account)
            .where(Account.email == email)
        )
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one_or_none()
        return row is not None

    async def get_accounts(self) -> list[XAccount]:
        req = (
            select(Account)
            .limit(10)
        )
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
                    is_banned=row.is_banned,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                    blocked_at=row.blocked_at,
                    blocked_till=row.blocked_till,
                )
            )
        return res

    async def delete_acc(self, acc_id: UUID) -> None:
        req = delete(Account).where(Account.id == acc_id)
        await self.session.execute(req)
        await self.session.commit()
