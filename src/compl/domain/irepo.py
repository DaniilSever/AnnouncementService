from uuid import UUID

from domain.compl.dto import QCreateCompl, QFilter

from domain.compl.models import Service

from infra.compl.xdao import XCompl


class IComplRepo:
    """Интерфейс репозитория для работы с жалобами."""

    async def create_compl(self, req: QCreateCompl) -> XCompl:
        """Создаёт новую жалобу.

        Args:
            req (QCreateCompl): Запрос на создание жалобы.

        Returns:
            XCompl: Созданная жалоба.
        """
        raise NotImplementedError

    async def get_my_complaint(self, compl_id: UUID, acc_id: UUID) -> XCompl:
        """Получает конкретную жалобу пользователя по ID.

        Args:
            compl_id (UUID): ID жалобы.
            acc_id (UUID): ID аккаунта автора жалобы.

        Returns:
            XCompl: Жалоба пользователя.
        """
        raise NotImplementedError

    async def get_my_complaints(
        self, acc_id: UUID, complaints_of: Service | None = None
    ) -> list[XCompl]:
        """Получает список жалоб пользователя с возможной фильтрацией по сервису.

        Args:
            acc_id (UUID): ID аккаунта автора жалоб.
            complaints_of (Service | None): Сервис, по которому фильтровать жалобы.

        Returns:
            list[XCompl]: Список жалоб пользователя.
        """
        raise NotImplementedError

    async def adm_get_complaint(self, compl_id: UUID) -> XCompl:
        """Получает конкретную жалобу по ID для админа.

        Args:
            compl_id (UUID): ID жалобы.

        Returns:
            XCompl: Жалоба для админского просмотра.
        """
        raise NotImplementedError

    async def adm_get_complaints(self, qfilter: QFilter) -> list[XCompl]:
        """Получает список жалоб с фильтрацией для админа.

        Args:
            qfilter (QFilter): Параметры фильтрации.

        Returns:
            list[XCompl]: Список жалоб.
        """
        raise NotImplementedError
