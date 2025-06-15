from uuid import UUID
from core.configs import AccountConfig
from core.exception import ExpError, ExpCode
from domain.account.irepo import IAccRepo
from domain.account.dto import (
    BannedTo,
    # QDTO
    QEmailSignupData,
    QEmail,
    # ZDTO
    ZAccount,
    ZAccountID,
    ZIsBusy,
)
from domain.account.models import AccRole
from domain.compl.dto import QCreateCompl, ZCompl
from infra.account.repo import AccRepo
from infra.account.xdao import XAccount
from services.ads.svc import AdsService
from services.compl.svc import ComplService
from services.tg.client import TgClient
from services.tg.const_msg import get_acc_ban_warning_msg, get_acc_unban_warning_msg


class AccUseCase:
    """Реализует бизнес-логику работы с аккаунтами, используя репозиторий.

    Args:
        _repo (AccRepo): Репозиторий аккаунтов.
        _ads_svc (AdsService): Сервис для работы с объявлениями.
        _compl_svc (ComplService): Сервис для работы с жалобами.
        _tg_svc (TgClient): Клиент для отправки сообщений в Telegram.
    """

    def __init__(
        self,
        _repo: AccRepo,
        _ads_svc: AdsService,
        _compl_svc: ComplService,
        _tg_svc: TgClient,
    ):
        self.cfg = AccountConfig()
        self.repo: IAccRepo = _repo
        self.ads_svc: AdsService = _ads_svc
        self.compl_svc: ComplService = _compl_svc
        self.tg_svc: TgClient = _tg_svc

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
        """Получает текущий аккаунт с количеством объявлений.

        Args:
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            ZAccount: Валидированная модель аккаунта.
        """
        try:
            count_ads = await self.ads_svc.get_count_ads_by_acc_id(acc_id)
        except ExpError as e:
            raise e

        x_acc = await self.repo.get_current_account(count_ads, acc_id)
        return ZAccount.model_validate(x_acc.model_dump(mode="json"))

    async def set_role_account(self, acc_id: UUID, role: AccRole) -> bool:
        """Устанавливает роль аккаунта.

        Args:
            acc_id (UUID): Идентификатор аккаунта.
            role (AccRole): Роль для установки.

        Returns:
            bool: Успешность операции.

        Raises:
            ExpError: Если аккаунт не найден.
        """
        try:
            await self.repo.set_role_account(acc_id, role)
        except KeyError as e:
            raise ExpError(ExpCode.ACC_ACCOUNT_NOT_FOUND, str(e)) from e
        return True

    async def set_ban_account(
        self, acc_id: UUID, blocked_to: BannedTo, reason_banned: str
    ) -> bool:
        """Блокирует аккаунт с указанием причины.

        Args:
            acc_id (UUID): Идентификатор аккаунта.
            blocked_to (BannedTo): Тип блокировки.
            reason_banned (str): Причина блокировки.

        Returns:
            bool: Успешность операции.

        Raises:
            ExpError: Если аккаунт не найден.
        """
        xacc = await self.get_account_by_id(acc_id)
        try:
            res = await self.repo.set_ban_account(acc_id, blocked_to, reason_banned)
        except KeyError as e:
            raise ExpError(ExpCode.ACC_ACCOUNT_NOT_FOUND, str(e)) from e

        msg = await get_acc_ban_warning_msg(
            str(xacc.email), blocked_to.value, str(res), reason_banned
        )
        await self.tg_svc.send_message(msg)

        return True

    async def set_unban_account(self, acc_id: UUID) -> bool:
        """Снимает блокировку с аккаунта.

        Args:
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            bool: Успешность операции.

        Raises:
            ExpError: Если аккаунт не найден.
        """
        xacc = await self.get_account_by_id(acc_id)
        try:
            await self.repo.set_unban_account(acc_id)
        except KeyError as e:
            raise ExpError(ExpCode.ACC_ACCOUNT_NOT_FOUND, str(e)) from e
        msg = await get_acc_unban_warning_msg(str(xacc.email))
        await self.tg_svc.send_message(msg)
        return True

    async def send_complaint(self, req: QCreateCompl) -> ZCompl:
        """Обрабатывает создание жалобы.

        Args:
            req (QCreateCompl): Данные жалобы.

        Returns:
            ZCompl: Результат создания жалобы.

        Raises:
            ExpError: При ошибках создания жалобы.
        """
        try:
            res = await self.compl_svc.create_compl(req)
        except ExpError as e:
            raise e
        return res
