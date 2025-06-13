from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete, update, text
from sqlalchemy.exc import IntegrityError

from domain.auth.irepo import IAuthRepo
from domain.auth.models import SignupAccount

from .xdao import XEmailSignup

class AuthRepo(IAuthRepo):
    """_"""

    def __init__(self, _session: AsyncSession):
        self.session: AsyncSession = _session

    async def create_email_signup(self, email: str, pwd_hash: str, salt: str, code: int) -> XEmailSignup:
        req = (
            insert(SignupAccount)
            .values(
                email=email,
                pwd_hash=pwd_hash,
                salt=salt,
                code=code,
            )
            .on_conflict_do_update(
                index_elements=["email"],
                set_={
                    "code": code,
                    "confirm_attempts": SignupAccount.confirm_attempts + 1,
                    "updated_at": text("CURRENT_TIMESTAMP(6)"),
                },
            )
            .returning(SignupAccount)
        )
        try:
            res = await self.session.execute(req)
        except IntegrityError as e:
            await self.session.rollback()
            raise RecursionError from e

        await self.session.commit()
        row = res.scalar_one()
        return XEmailSignup(
            id=row.id,
            email=row.email,
            pwd_hash=row.pwd_hash,
            salt=row.salt,
            code=row.code,
            created_at=row.created_at,
            updated_at=row.updated_at,
            blocked_till=row.blocked_till,
            confirm_attempts=row.confirm_attempts,
        )

    async def get_email_signup(self, signup_id: UUID) -> XEmailSignup:
        req = (
            select(SignupAccount)
            .where(SignupAccount.id == signup_id)
        )
        res = await self.session.execute(req)
        return res.scalar_one_or_none()

    async def delete_email_signup(self, signup_id: UUID) -> None:
        req = delete(SignupAccount).where(SignupAccount.id == signup_id)
        await self.session.execute(req)
        await self.session.commit()

    async def inc_email_confirm_wrong_code_attempts(self, signup_id: UUID) -> XEmailSignup:
        req = (
            update(SignupAccount)
            .values(
                confirm_attempts=SignupAccount.confirm_attempts + 1,
                updated_at=datetime.now()
            )
            .where(SignupAccount.id == signup_id)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(req)
        await self.session.commit()
        await self.session.refresh(req)
        return XEmailSignup(
            id=req.id,
            email=req.email,
            pwd_hash=req.pwd_hash,
            salt=req.salt,
            code=req.code,
            created_at=req.created_at,
            updated_at=req.updated_at,
            blocked_till=req.blocked_till,
            confirm_attempts=req.confirm_attempts,
        )

    async def block_email_confirm_by_email(self, email: str) -> XEmailSignup:
        req = (
            update(SignupAccount)
            .values(
                updated_at=text("CURRENT_TIMESTAMP(6)"),
                blocked_till=text("CURRENT_TIMESTAMP(6) + INTERVAL '1 DAYS'"),
            )
            .where(SignupAccount.email == email)
            .execution_options(synchronize_session="fetch")
            .returning(SignupAccount)
        )
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one()
        return XEmailSignup(
            id=row.id,
            email=row.email,
            pwd_hash=row.pwd_hash,
            salt=row.salt,
            code=row.code,
            created_at=row.created_at,
            updated_at=row.updated_at,
            blocked_till=row.blocked_till,
            confirm_attempts=row.confirm_attempts,
        )
