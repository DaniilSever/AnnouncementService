from uuid import UUID

class IAccRepo:
    """Интерфейс репозитория для работы с пользовательскими аккаунтами"""

    async def get_account_by_id(self, acc_id: UUID):
        """Получает аккаунт по его ID.

        Args:
            acc_id (UUID): Уникальный идентификатор аккаунта.

        Returns:
            Account: Объект аккаунта.
        """

        raise NotImplementedError

    async def get_account_by_email(self, email: str):
        """Получает аккаунт по email.

        Args:
            email (str): Электронная почта пользователя.

        Returns:
            Account: Объект аккаунта.
        """

        raise NotImplementedError

    async def copy_account_from_signup(self, x_signup):
        """Копирует данные из временной регистрации в аккаунт.

        Args:
            x_signup (SignupData): Данные временной регистрации.

        Returns:
            Account: Созданный аккаунт.
        """

        raise NotImplementedError

    async def is_email_busy(self, email: str):
        """Проверяет, занят ли email.

        Args:
            email (str): Электронная почта для проверки.

        Returns:
            bool: True, если email занят, иначе False.
        """

        raise NotImplementedError

    async def get_accounts(self) -> list:
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
