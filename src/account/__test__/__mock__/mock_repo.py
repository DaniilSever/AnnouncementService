from uuid import UUID

from account.domain.irepo import IAccRepo
from account.domain.dto import QEmailSignupData
from account.domain.models import AccRole
from account.infra.xdao import XAccount, XAccountID

class MockAccRepo(IAccRepo):
    """Мокк работы с бд"""

    def __init__(self, *args):
        pass

    async def get_account_by_id(self, count_ads: int, acc_id: UUID) -> XAccount:
        """Получает аккаунт по его ID.

        Args:
            count_ads (int): Количество объявлений для выборки (например, для вложенных данных).
            acc_id (UUID): Уникальный идентификатор аккаунта.

        Returns:
            XAccount: Объект аккаунта.
        """
        return XAccount(
            id="6dda82b8-72dd-42f4-af43-8dedd2dc2520",
            email="test@example.com",
            pwd_hash="e1ee98334d5bfd0810fa6c03beef3cc3d05486a56c9d32e9b528d9af4477e3fa",
            salt="a9330649b51c9ed1d905fddeabd606f7",
            role=AccRole.USER,
            count_ads=0,
        )

    async def get_account_by_email(self, email: str, count_ads: int | None = None) -> XAccount:
        """Получает аккаунт по email.

        Args:
            email (str): Электронная почта пользователя.
            count_ads (int | None): Количество объявлений для выборки (необязательно).

        Returns:
            XAccount: Объект аккаунта.
        """
        return XAccount(
            id="6dda82b8-72dd-42f4-af43-8dedd2dc2520",
            email="test@example.com",
            pwd_hash="e1ee98334d5bfd0810fa6c03beef3cc3d05486a56c9d32e9b528d9af4477e3fa",
            salt="a9330649b51c9ed1d905fddeabd606f7",
            role=AccRole.USER,
            count_ads=0,
        )

    async def copy_account_from_signup(self, x_signup: QEmailSignupData) -> XAccountID:
        """Копирует данные из временной регистрации в аккаунт.

        Args:
            x_signup (QEmailSignupData): Данные временной регистрации.

        Returns:
            XAccountID: Созданный аккаунт с ID.
        """
        return XAccountID(id="6dda82b8-72dd-42f4-af43-8dedd2dc2520")

    async def is_email_busy(self, email: str) -> bool:
        """Проверяет, занят ли email.

        Args:
            email (str): Электронная почта для проверки.

        Returns:
            bool: True, если email занят, иначе False.
        """
        return True

    async def get_accounts(self) -> list[XAccount]:
        """Возвращает список всех аккаунтов.

        Returns:
            list[XAccount]: Список объектов аккаунтов.
        """
        return [
            XAccount(
                id="6dda82b8-72dd-42f4-af43-8dedd2dc2520",
                email="test1@example.com",
                pwd_hash="e1ee98334d5bfd0810fa6c03beef3cc3d05486a56c9d32e9b528d9af4477e3fa",
                salt="a9330649b51c9ed1d905fddeabd606f7",
                role=AccRole.USER,
                count_ads=0,
            ),
            XAccount(
                id="5d5ac71c-018f-4058-86ed-59d7d6a28464",
                email="test2@example.com",
                pwd_hash="e1ee98334d5bfd0810fa6c03beef3cc3d05486a56c9d32e9b528d9af4477e3fa",
                salt="a9330649b51c9ed1d905fddeabd606f7",
                role=AccRole.USER,
                count_ads=0,
            ),
        ]

    async def delete_acc(self, acc_id: UUID) -> None:
        """Удаляет аккаунт по ID.

        Args:
            acc_id (UUID): Уникальный идентификатор аккаунта.

        Returns:
            None
        """
        return

    async def get_current_account(self, count_ads: int, acc_id: UUID) -> XAccount:
        """Получает текущий аккаунт по ID с учётом количества объявлений.

        Args:
            count_ads (int): Количество объявлений для выборки.
            acc_id (UUID): Уникальный идентификатор аккаунта.

        Returns:
            XAccount: Объект текущего аккаунта.
        """
        return XAccount(
            id="5d5ac71c-018f-4058-86ed-59d7d6a28464",
            email="test2@example.com",
            pwd_hash="e1ee98334d5bfd0810fa6c03beef3cc3d05486a56c9d32e9b528d9af4477e3fa",
            salt="a9330649b51c9ed1d905fddeabd606f7",
            role=AccRole.USER,
            count_ads=0,
        )
