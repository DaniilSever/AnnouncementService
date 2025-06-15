from uuid import UUID
from core.configs import AccountConfig
from core.exception import ExpError, ExpCode
from domain.account.irepo import IAccRepo
from domain.account.dto import QEmailSignupData, QEmail
from domain.account.dto import ZAccount, ZAccountID, ZIsBusy
from infra.account.repo import AccRepo
from infra.account.xdao import XAccount
from services.ads.svc import AdsService


class AccUseCase:
    """Реализует бизнес-логику работы с аккаунтами, используя репозиторий."""

    def __init__(self, _repo: AccRepo, _ads_svc: AdsService):
        """Инициализирует use case с репозиторием аккаунтов.

        Args:
            _repo (AccRepo): Репозиторий аккаунтов.
            _acc_svc (AccService): Сервис для работы с аккаунтами.
        """
        self.cfg = AccountConfig()
        self.repo: IAccRepo = _repo
        self.ads_svc: AdsService = _ads_svc

    async def get_account_by_id(self, acc_id: UUID) -> ZAccount:
        """Получает аккаунт по его ID.

        Args:
            acc_id (UUID): Уникальный идентификатор аккаунта.

        Returns:
            ZAccount: Валидированная модель аккаунта.

        Raises:
            ExpError: Если аккаунт не найден.
        """
        try:
            count_ads = await self.ads_svc.get_count_ads_by_acc_id(acc_id)
        except ExpError as e:
            raise e

        try:
            x_acc: XAccount = await self.repo.get_account_by_id(count_ads, acc_id)
        except KeyError as e:
            raise ExpError(ExpCode.ACC_ACCOUNT_NOT_FOUND, str(e)) from e
        return ZAccount.model_validate(x_acc.model_dump(mode="json"))

    async def get_account_by_email(self, req: QEmail) -> ZAccount:
        """Получает аккаунт по email.

        Args:
            req (QEmail): Запрос с email пользователя.

        Returns:
            ZAccount: Валидированная модель аккаунта.

        Raises:
            ExpError: Если аккаунт не найден.
        """
        try:
            x_acc: XAccount = await self.repo.get_account_by_email(req.email)
        except KeyError as e:
            raise ExpError(ExpCode.ACC_ACCOUNT_NOT_FOUND, str(e)) from e

        try:
            count_ads = await self.ads_svc.get_count_ads_by_acc_id(x_acc.id)
        except ExpError as e:
            raise e

        try:
            x_acc: XAccount = await self.repo.get_account_by_email(req.email, count_ads)
        except KeyError as e:
            raise ExpError(ExpCode.ACC_ACCOUNT_NOT_FOUND, str(e)) from e

        return ZAccount.model_validate(x_acc.model_dump(mode="json"))

    async def copy_account_from_signup(self, signup: QEmailSignupData) -> ZAccountID:
        """Создаёт аккаунт на основе данных временной регистрации.

        Args:
            signup (QEmailSignupData): Данные временной регистрации.

        Returns:
            ZAccountID: Идентификатор созданного аккаунта.
        """
        xacc_id = await self.repo.copy_account_from_signup(signup)
        return ZAccountID(id=xacc_id.id)

    async def is_email_busy(self, req: QEmail) -> ZIsBusy:
        """Проверяет, занят ли email.

        Args:
            req (QEmail): Запрос с email для проверки.

        Returns:
            ZIsBusy: Статус занятости email.
        """
        is_busy = await self.repo.is_email_busy(req.email)
        return ZIsBusy(is_busy=is_busy)

    async def get_accounts(self) -> list[ZAccount]:
        """Получает список аккаунтов.

        Returns:
            list[ZAccount]: Список валидированных аккаунтов.
        """
        xres = await self.repo.get_accounts()
        res = []
        for xacc in xres:
            res.append(ZAccount(**xacc.model_dump(mode="json")))
        return res

    async def get_current_account(self, acc_id: UUID) -> ZAccount:
        try:
            count_ads = await self.ads_svc.get_count_ads_by_acc_id(acc_id)
        except ExpError as e:
            raise e
        print(count_ads)
        x_acc = await self.repo.get_current_account(count_ads, acc_id)
        return ZAccount.model_validate(x_acc.model_dump(mode="json"))
