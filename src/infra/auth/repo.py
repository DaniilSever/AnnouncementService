from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from domain.auth.irepo import IAuthRepo
from domain.auth.models import SignupAccount

from .xdao import XEmailSignup

class AuthRepo(IAuthRepo):
    """_"""

    def __init__(self, _session: AsyncSession):
        self.session: AsyncSession = _session

    async def create_email_signup(self, email: str, pwd_hash: str, salt: str, code: int) -> XEmailSignup:
        req = SignupAccount(
            email=email,
            pwd_hash=pwd_hash,
            salt=salt,
            code=code,
        )
        self.session.add(req)
        await self.session.commit()
        await self.session.refresh(req)
        return XEmailSignup(**req)

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
        return XEmailSignup(**req)

    async def block_email_confirm_by_email(self, email: str) -> XEmailSignup:
        req = (
            update(SignupAccount)
            .values(expired_at=datetime.now() + timedelta(days=1))
            .where(SignupAccount.email == email)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(req)
        await self.session.commit()
        await self.session.refresh(req)
        return XEmailSignup(**req)
