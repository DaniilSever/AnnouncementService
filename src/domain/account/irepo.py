from uuid import UUID

from domain.account.dto import QEmailSignupData
from infra.account.xdao import XAccount, XAccountID


class IAccRepo:
    """Интерфейс репозитория для работы с пользовательскими аккаунтами"""

    async def get_account_by_id(self, count_ads: int, acc_id: UUID) -> XAccount:
        """Получает аккаунт по его ID.

        Args:
            acc_id (UUID): Уникальный идентификатор аккаунта.

        Returns:
            Account: Объект аккаунта.
        """

        raise NotImplementedError

    async def get_account_by_email(self, email: str, count_ads: int | None = None) -> XAccount:
        """Получает аккаунт по email.

        Args:
            email (str): Электронная почта пользователя.

        Returns:
            Account: Объект аккаунта.
        """

        raise NotImplementedError

    async def copy_account_from_signup(self, x_signup: QEmailSignupData) -> XAccountID:
        """Копирует данные из временной регистрации в аккаунт.

        Args:
            x_signup (SignupData): Данные временной регистрации.

        Returns:
            Account: Созданный аккаунт.
        """

        raise NotImplementedError

    async def is_email_busy(self, email: str) -> bool:
        """Проверяет, занят ли email.

        Args:
            email (str): Электронная почта для проверки.

        Returns:
            bool: True, если email занят, иначе False.
        """

        raise NotImplementedError

    async def get_accounts(self) -> list[XAccount]:
        """Возвращает список всех аккаунтов.

        Returns:
            list: Список объектов аккаунтов.
        """

        raise NotImplementedError

    async def delete_acc(self, acc_id: UUID) -> None:
        """Удаляет аккаунт по ID.

        Args:
            acc_id (UUID): Уникальный идентификатор аккаунта.

        Returns:
            None
        """

        raise NotImplementedError

    async def get_current_account(self, count_ads: int, acc_id: UUID) -> XAccount:
        raise NotImplementedError
