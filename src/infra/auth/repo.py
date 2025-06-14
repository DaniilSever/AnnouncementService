from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete, update, text
from sqlalchemy.exc import IntegrityError

from domain.auth.irepo import IAuthRepo
from domain.auth.models import SignupAccount, RefreshToken

from .xdao import XEmailSignup, XRefreshToken

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
                    "attempts": SignupAccount.attempts + 1,
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
            attempts=row.attempts,
        )

    async def get_email_signup(self, signup_id: UUID) -> XEmailSignup:
        req = (
            select(SignupAccount)
            .where(SignupAccount.id == signup_id)
        )
        res = await self.session.execute(req)
        row = res.scalar_one_or_none()
        if row is None:
            raise KeyError("Отсутствует запись на регистрацию")
        return XEmailSignup(
            id=row.id,
            email=row.email,
            pwd_hash=row.pwd_hash,
            salt=row.salt,
            code=row.code,
            created_at=row.created_at,
            updated_at=row.updated_at,
            blocked_till=row.blocked_till,
            attempts=row.attempts,
        )

    async def delete_email_signup(self, signup_id: UUID) -> None:
        req = delete(SignupAccount).where(SignupAccount.id == signup_id)
        await self.session.execute(req)
        await self.session.commit()

    async def inc_email_confirm_wrong_code_attempts(self, signup_id: UUID) -> XEmailSignup:
        req = (
            update(SignupAccount)
            .values(
                attempts=SignupAccount.attempts + 1,
                updated_at=text("CURRENT_TIMESTAMP(6)")
            )
            .where(SignupAccount.id == signup_id)
            .execution_options(synchronize_session="fetch")
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
            attempts=row.attempts,
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
            attempts=row.attempts,
        )

    async def get_refresh_token_for_account(self, acc_id: UUID, token: str) -> XRefreshToken:
        """Получает refresh-токен по аккаунту и значению токена"""
        req = (
            select(RefreshToken)
            .where(
                RefreshToken.account_id == acc_id,
                RefreshToken.token == token,
                RefreshToken.is_revoked is False,
                RefreshToken.expires_at > text("NOW()")
            )
        )
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one_or_none()
        if row is None:
            raise KeyError("Отсутствует токен в базе")
        return XRefreshToken(
            id=row.id,
            account_id=row.account_id,
            token=row.token,
            is_revoked=row.is_revoked,
            created_at=row.created_at,
            expires_at=row.expires_at
        )

    async def revoke_expired_tokens(self) -> None:
        """Удаляет или инвалидирует просроченные refresh-токены"""
        req = delete(RefreshToken).where(RefreshToken.expires_at < text("NOW()"))
        await self.session.execute(req)
        await self.session.commit()

    async def save_refresh_token(self, acc_id: UUID, token: str) -> XRefreshToken:
        """Сохраняет refresh-токен для аккаунта"""
        req = (
            insert(RefreshToken)
            .values(
                account_id=acc_id,
                token=token,
                expires_at=text("NOW() + INTERVAL '7 DAYS'")
            )
            .returning(RefreshToken)
        )
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one()
        return XRefreshToken(
            id=row.id,
            account_id=row.account_id,
            token=row.token,
            is_revoked=row.is_revoked,
            created_at=row.created_at,
            expires_at=row.expires_at
        )

    async def revoke_tokens(self, acc_id: UUID) -> int:
        """Инвалидирует все refresh-токены для аккаунта"""
        req = (
            update(RefreshToken)
            .values(
                is_revoked=True,
            )
            .where(
                RefreshToken.acc_id == acc_id,
                RefreshToken.is_revoked is False
            )
        )
        res = await self.session.execute(req)
        await self.session.commit()
        return res.rowcount
