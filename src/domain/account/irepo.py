from uuid import UUID

class IAccRepo:
    """Интерфейс репозитория для работы с пользовательскими аккаунтами"""

    async def get_account_by_id(self, acc_id: UUID):
        """Получает аккаунт по его ID"""
        raise NotImplementedError

    async def get_account_by_email(self, email: str):
        """Получает аккаунт по email"""
        raise NotImplementedError

    async def copy_account_from_signup(self, x_signup):
        """Копирует данные из временной регистрации в аккаунт"""
        raise NotImplementedError

    async def is_email_busy(self, email: str):
        """Проверяет, занят ли email"""
        raise NotImplementedError

    async def get_accounts(self) -> list:
        """Возвращает список всех аккаунтов"""
        raise NotImplementedError

    async def delete_acc(self, acc_id: UUID) -> None:
        """Удаляет аккаунт по ID"""
        raise NotImplementedError
