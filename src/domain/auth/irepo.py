from uuid import UUID

from infra.auth.xdao import XEmailSignup, XRefreshToken


class IAuthRepo:  # pragma: no cover
    """Интерфейс репозитория для операций, связанных с аутентификацией и управлением токенами."""

    async def create_email_signup(
        self, email: str, pwd_hash: str, salt: str, code: int
    ) -> XEmailSignup:
        """Создаёт запись регистрации по email.

        Args:
            email (str): Электронная почта пользователя.
            pwd_hash (str): Хэш пароля.
            salt (str): Соль для хэша пароля.
            code (int): Код подтверждения.

        Returns:
            XEmailSignup: Созданная запись регистрации.
        """
        raise NotImplementedError

    async def get_email_signup(self, signup_id: UUID) -> XEmailSignup:
        """Получает данные регистрации по её ID.

        Args:
            signup_id (UUID): Идентификатор регистрации.

        Returns:
            XEmailSignup: Данные регистрации.
        """
        raise NotImplementedError

    async def delete_email_signup(self, signup_id: UUID) -> None:
        """Удаляет запись регистрации по её ID.

        Args:
            signup_id (UUID): Идентификатор регистрации.
        """
        raise NotImplementedError

    async def inc_email_confirm_wrong_code_attempts(
        self, signup_id: UUID
    ) -> XEmailSignup:
        """Увеличивает счётчик неверных попыток ввода кода подтверждения по email.

        Args:
            signup_id (UUID): Идентификатор регистрации.

        Returns:
            XEmailSignup: Обновлённая запись регистрации.
        """
        raise NotImplementedError

    async def block_email_confirm_by_email(self, email: str) -> XEmailSignup:
        """Блокирует подтверждение email.

        Args:
            email (str): Электронная почта пользователя.

        Returns:
            XEmailSignup: Обновлённая запись регистрации с блокировкой.
        """
        raise NotImplementedError

    async def get_refresh_token_for_account(
        self, acc_id: UUID, token: str
    ) -> XRefreshToken:
        """Получает refresh-токен по аккаунту и значению токена.

        Args:
            acc_id (UUID): Идентификатор аккаунта.
            token (str): Значение refresh-токена.

        Returns:
            XRefreshToken: Найденный refresh-токен.
        """
        raise NotImplementedError

    async def revoke_expired_tokens(self) -> None:
        """Удаляет или инвалидирует просроченные refresh-токены."""
        raise NotImplementedError

    async def save_refresh_token(self, acc_id: UUID, token: str) -> XRefreshToken:
        """Сохраняет refresh-токен для аккаунта.

        Args:
            acc_id (UUID): Идентификатор аккаунта.
            token (str): Значение refresh-токена.

        Returns:
            XRefreshToken: Сохранённый refresh-токен.
        """
        raise NotImplementedError

    async def revoke_tokens(self, acc_id: UUID) -> int:
        """Инвалидирует все refresh-токены для аккаунта.

        Args:
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            int: Количество инвалидированных токенов.
        """
        raise NotImplementedError
