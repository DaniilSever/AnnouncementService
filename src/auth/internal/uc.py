from datetime import datetime

from kernel.configs import AuthConfig
from kernel.security import (
    create_confirm_code,
    create_password_hash,
    create_jwt_token,
    decode_jwt,
)
from kernel.exception import ExpError, ExpCode

from ..domain.dto import (
    # QDTO
    QEmailSignup,
    QConfirmCode,
    QEmailSignin,
    QRefreshToken,
    QRevokeToken,
    # ZDTO
    ZEmailSignup,
    ZAccountID,
    ZToken,
    ZRevokedTokens,
)
from ..domain.irepo import IAuthRepo
from account.domain.dto import (
    # QDTO
    QEmailSignupData,
    # ZDTO
    ZAccount,
)

from ..infra.repo import AuthRepo
from ..infra.xdao import XEmailSignup

from account.external.svc import AccService
from notice.external.tg.client import TgClient
from notice.external.tg.const_msg import get_code_msg


class AuthUseCase:
    """Управляет бизнес-логикой аутентификации и авторизации.

    Args:
        _repo (AuthRepo): Репозиторий для работы с данными аутентификации.
        _acc_svc (AccService): Сервис для работы с аккаунтами.
        _tg_svc (TgClient): Клиент Telegram для отправки сообщений.
    """

    def __init__(self, _repo: AuthRepo, _acc_svc: AccService, _tg_svc: TgClient):
        self.cfg = AuthConfig()
        self.repo: IAuthRepo = _repo
        self.acc_svc: AccService = _acc_svc
        self.tg_svc: TgClient = _tg_svc

    async def signup_email(self, req: QEmailSignup) -> ZEmailSignup:
        """Создаёт заявку на регистрацию по email.

        Args:
            req (QEmailSignup): Данные для регистрации.

        Returns:
            ZEmailSignup: Результат создания заявки.
        """

        if await self.acc_svc.is_email_busy(req.email):
            raise ExpError(ExpCode.ACC_EMAIL_IS_BUSY)

        code = create_confirm_code()
        pwd_hash, salt = create_password_hash(req.password)

        try:
            x_signup: XEmailSignup = await self.repo.create_email_signup(
                req.email, pwd_hash, salt, code
            )
        except RecursionError as e:
            x_signup: XEmailSignup = await self.repo.block_email_confirm_by_email(
                req.email
            )
            raise ExpError(ExpCode.AUTH_MANY_REGISTRATION_ATTEMPTS, str(e)) from e

        msg = await get_code_msg(str(req.email), str(code))
        await self.tg_svc.send_message(msg)

        return ZEmailSignup.model_validate(x_signup.model_dump(mode="json"))

    async def confirm_email(self, req: QConfirmCode) -> ZAccountID:
        """Подтверждает регистрацию по email с помощью кода подтверждения.

        Args:
            req (QConfirmCode): Запрос с ID заявки и кодом подтверждения.

        Returns:
            ZAccountID: Идентификатор созданного аккаунта.
        """

        try:
            x_signup: XEmailSignup = await self.repo.get_email_signup(req.signup_id)
        except KeyError as e:
            raise ExpError(ExpCode.AUTH_SINGUP_NOT_FOUND, str(e)) from e

        if self._is_blocked(x_signup.blocked_till):
            raise ExpError(ExpCode.AUTH_EMAIL_BLOCKED)

        if req.code != x_signup.code:
            try:
                await self.repo.inc_email_confirm_wrong_code_attempts(x_signup.id)
            except RecursionError as e:
                await self.repo.block_email_confirm_by_email(x_signup.email)
                raise ExpError(ExpCode.AUTH_MANY_CONFIRMATION_ATTEMPTS, str(e)) from e
            raise ExpError(ExpCode.AUTH_WRONG_CODE)

        try:
            signup = QEmailSignupData(**x_signup.model_dump(mode="json"))
            acc_id = await self.acc_svc.copy_account_from_signup(signup)
        except ExpError as e:
            raise e

        await self.repo.delete_email_signup(x_signup.id)
        return ZAccountID(id=acc_id)

    async def signin_email(self, req: QEmailSignin) -> ZToken:
        """Выполняет вход пользователя по email и паролю.

        Args:
            req (QEmailSignin): Данные для входа.

        Returns:
            ZToken: Access- и refresh-токены сессии.
        """
        try:
            z_acc: ZAccount = await self.acc_svc.get_account_by_email(req.email)
        except ExpError as e:
            raise e

        pwd_hash, _ = create_password_hash(req.password, salt=z_acc.salt)
        if pwd_hash != z_acc.pwd_hash:
            raise ExpError(ExpCode.AUTH_SIGNIN_WRONG_PASSWORD)

        access_payload = {
            "acc_id": str(z_acc.id),
            "role": str(z_acc.role.value),
            "is_banned": str(z_acc.is_banned),
            "blocked_at": str(z_acc.blocked_at),
            "reason_blocked": str(z_acc.reason_blocked),
            "blocked_to": str(z_acc.blocked_to),
            "type": "access",
        }
        access_token = create_jwt_token(
            access_payload, self.cfg.JWT_PRIVATE_KEY, delta=3600
        )

        refresh_payload = {
            "acc_id": str(z_acc.id),
            "role": str(z_acc.role.value),
            "is_banned": str(z_acc.is_banned),
            "blocked_at": str(z_acc.blocked_at),
            "reason_blocked": str(z_acc.reason_blocked),
            "blocked_to": str(z_acc.blocked_to),
            "type": "access",
        }
        refresh_token = create_jwt_token(
            refresh_payload, self.cfg.JWT_PRIVATE_KEY, delta=7 * 24 * 60 * 60
        )

        await self.repo.save_refresh_token(
            acc_id=z_acc.id,
            token=refresh_token,
        )
        return ZToken(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(self, req: QRefreshToken) -> ZToken:
        """Обновляет access-токен с использованием refresh-токена.

        Args:
            req (QRefreshToken): Запрос с refresh-токеном.

        Returns:
            ZToken: Новый access-токен и переданный refresh-токен.
        """
        await self.repo.revoke_expired_tokens()

        payload = await decode_jwt(req.refresh_token, self.cfg.JWT_PUBLIC_KEY)
        if payload.get("type") != "refresh":
            raise ExpError(ExpCode.AUTH_INVALID_TOKEN_TYPE)

        try:
            _ = await self.repo.get_refresh_token_for_account(
                payload["acc_id"], req.refresh_token
            )
        except KeyError as e:
            raise ExpError(ExpCode.AUTH_REFRESH_TOKEN_NOT_FOUND, str(e)) from e

        access_payload = {
            "acc_id": payload["acc_id"],
            "role": payload["role"],
            "is_banned": payload["is_banned"],
            "blocked_at": payload["blocked_at"],
            "reason_blocked": payload["reason_blocked"],
            "blocked_to": payload["blocked_to"],
        }
        access_token = create_jwt_token(
            access_payload, self.cfg.JWT_PRIVATE_KEY, delta=3600
        )

        return ZToken(access_token=access_token, refresh_token=req.refresh_token)

    async def revoke_token(self, req: QRevokeToken) -> ZRevokedTokens:
        """Отзывает все refresh-токены аккаунта.

        Args:
            req (QRevokeToken): Запрос с ID аккаунта.

        Returns:
            ZRevokedTokens: Результат отзыва токенов.
        """
        count = await self.repo.revoke_tokens(acc_id=req.account_id)

        if count == 0:
            raise ExpError(ExpCode.AUTH_REVOKE_TOKEN_NOT_FOUND)

        return ZRevokedTokens(message=f"Успешно отозван(ы) {count} токен(ы) ")

    # ------------------ Tools ------------------

    @staticmethod
    def _is_blocked(dt: datetime | None) -> bool:
        """Проверяет, заблокирована ли операция по времени блокировки.

        Args:
            dt (datetime | None): Дата и время окончания блокировки.

        Returns:
            bool: True, если операция заблокирована, иначе False.
        """
        if not dt:
            return False
        return dt > datetime.now()
