from uuid import UUID

from infra.auth.xdao import XEmailSignup

class IAuthRepo:  # pragma: no cover
    """Интерфейс репозитория для операций, связанных с аутентификацией и управлением токенами"""

    async def create_email_signup(self, email: str, pwd_hash: str, salt: str, code: int) -> XEmailSignup:
        """Создаёт запись регистрации по email"""
        raise NotImplementedError

    async def get_email_signup(self, signup_id: UUID) -> XEmailSignup:
        """Получает данные регистрации по её ID"""
        raise NotImplementedError

    async def delete_email_signup(self, signup_id: UUID) -> None:
        """Удаляет запись регистрации по её ID"""
        raise NotImplementedError

    async def inc_email_confirm_wrong_code_attempts(self, signup_id: UUID) -> XEmailSignup:
        """Увеличивает счётчик неверных попыток ввода кода подтверждения по email"""
        raise NotImplementedError

    async def block_email_confirm_by_email(self, email: str) -> XEmailSignup:
        """Блокирует подтверждение email"""
        raise NotImplementedError

    async def get_refresh_token_for_account(self, acc_id: UUID, token: str):
        """Получает refresh-токен по аккаунту и значению токена"""
        raise NotImplementedError

    async def revoke_expired_tokens(self):
        """Удаляет или инвалидирует просроченные refresh-токены"""
        raise NotImplementedError

    async def save_refresh_token(self, acc_id: UUID, token: str):
        """Сохраняет refresh-токен для аккаунта"""
        raise NotImplementedError

    async def revoke_tokens(self, acc_id: UUID):
        """Инвалидирует все refresh-токены для аккаунта"""
        raise NotImplementedError
