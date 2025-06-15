from uuid import UUID

from domain.ads.dto import (
    QCreateAds,
    QAdsCategory,
    QFilter,
    QChangeAds,
    QAddAdsComment,
    QUpdateAdsComment,
)
from infra.ads.xdao import XAds, XAdsComment


class IAdsRepo:
    """Интерфейс репозитория для работы с объявлениями и комментариями."""

    async def create_ads(
        self, ads: QCreateAds, ads_category: QAdsCategory, acc_id: UUID | None = None
    ) -> XAds:
        """Создаёт объявление.

        Args:
            ads (QCreateAds): Данные объявления.
            ads_category (QAdsCategory): Категория объявления.
            acc_id (UUID | None): Идентификатор аккаунта (необязательно).

        Returns:
            XAds: Созданное объявление.
        """
        raise NotImplementedError

    async def get_ads_all(self, qfilter: QFilter) -> tuple[int, list[XAds]]:
        """Получает все объявления с фильтром.

        Args:
            qfilter (QFilter): Параметры фильтрации.

        Returns:
            tuple[int, list[XAds]]: Количество и список объявлений.
        """
        raise NotImplementedError

    async def get_ads_by_id(self, ads_id: UUID) -> XAds:
        """Получает объявление по его ID.

        Args:
            ads_id (UUID): Идентификатор объявления.

        Returns:
            XAds: Объявление.
        """
        raise NotImplementedError

    async def get_ads_by_account_id(self, acc_id: UUID) -> tuple[int, list[XAds]]:
        """Получает объявления по ID аккаунта.

        Args:
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            tuple[int, list[XAds]]: Количество и список объявлений.
        """
        raise NotImplementedError

    async def update_ads(self, new_ads: QChangeAds, acc_id: UUID) -> XAds:
        """Обновляет объявление.

        Args:
            new_ads (QChangeAds): Новые данные объявления.
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            XAds: Обновлённое объявление.
        """
        raise NotImplementedError

    async def update_category_ads(
        self, ads_id: UUID, new_category: QAdsCategory, acc_id: UUID
    ) -> XAds:
        """Обновляет категорию объявления.

        Args:
            ads_id (UUID): Идентификатор объявления.
            new_category (QAdsCategory): Новая категория.
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            XAds: Обновлённое объявление.
        """
        raise NotImplementedError

    async def delete_ads(self, ads_id: UUID, acc_id: UUID) -> None:
        """Удаляет объявление.

        Args:
            ads_id (UUID): Идентификатор объявления.
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            None
        """
        raise NotImplementedError

    async def get_count_ads_by_acc_id(self, acc_id: UUID) -> int:
        raise NotImplementedError

    async def create_ads_commentary(
        self, new_comment: QAddAdsComment, acc_id: UUID
    ) -> XAdsComment:
        """Создаёт комментарий к объявлению.

        Args:
            new_comment (QAddAdsComment): Данные комментария.
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            XAdsComment: Созданный комментарий.
        """
        raise NotImplementedError

    async def get_ads_commentaries(self, ads_id: UUID) -> tuple[int, list[XAdsComment]]:
        """Получает комментарии к объявлению.

        Args:
            ads_id (UUID): Идентификатор объявления.

        Returns:
            tuple[int, list[XAdsComment]]: Количество и список комментариев.
        """
        raise NotImplementedError

    async def get_ads_commentary(self, ads_id: UUID, comment_id: UUID) -> XAdsComment:
        """Получает конкретный комментарий к объявлению.

        Args:
            ads_id (UUID): Идентификатор объявления.
            comment_id (UUID): Идентификатор комментария.

        Returns:
            XAdsComment: Комментарий.
        """
        raise NotImplementedError

    async def update_ads_commentary(
        self, update_comm: QUpdateAdsComment
    ) -> XAdsComment:
        """Обновляет комментарий к объявлению.

        Args:
            update_comm (QUpdateAdsComment): Новые данные комментария.

        Returns:
            XAdsComment: Обновлённый комментарий.
        """
        raise NotImplementedError

    async def delete_ads_commentary(
        self, ads_id: UUID, comm_id: UUID, acc_id: UUID
    ) -> None:
        """Удаляет комментарий к объявлению.

        Args:
            ads_id (UUID): Идентификатор объявления.
            comm_id (UUID): Идентификатор комментария.
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            None
        """
        return NotImplementedError

    async def get_ads_id_by_comm_id(self, comm_id: UUID) -> UUID:
        return NotImplementedError

    async def adm_delete_ads_commentary(self, comm_id: UUID, ads_id: UUID) -> None:
        return NotImplementedError
