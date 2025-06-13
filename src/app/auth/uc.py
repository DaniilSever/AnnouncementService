from datetime import datetime
from core.configs import AuthConfig
from core.security import create_confirm_code, create_password_hash
from core.exception import ErrExp, ExpCode
from domain.auth.dto import QEmailSignup, QConfirmCode
from domain.auth.dto import ZEmailSignup, ZAccountID
from domain.auth.irepo import IAuthRepo
from infra.auth.repo import AuthRepo
from infra.auth.xdao import XEmailSignup


class AuthUseCase:

    def __init__(self, _repo: AuthRepo):
        self.cfg = AuthConfig()
        self.repo: IAuthRepo = _repo

    async def signup_email(self, req: QEmailSignup) -> ZEmailSignup:
        code = create_confirm_code()
        pwd_hash, salt = create_password_hash(req.password)

        try:
            x_signup: XEmailSignup = await self.repo.create_email_signup(req.email, pwd_hash, salt, code)
        except RecursionError as e:
            x_signup: XEmailSignup = await self.repo.block_email_confirm_by_email(req.email)
            raise ErrExp(ExpCode.AUTH_MANY_REGISTRATION_ATTEMPTS, str(e)) from e

        return ZEmailSignup.model_validate(x_signup.model_dump(mode="json"))

    async def confirm_email(self, req: QConfirmCode) -> ZAccountID:

        try:
            x_signup: XEmailSignup = await self.repo.get_email_signup(req.signup_id)
        except KeyError as e:
            raise ErrExp(ExpCode.AUTH_SINGUP_NOT_FOUND, str(e)) from e

        if self._is_blocked(x_signup.blocked_till):
            raise ErrExp(ExpCode.AUTH_EMAIL_BLOCKED)

        if req.code != x_signup.code:
            try:
                await self.repo.inc_email_confirm_wrong_code_attempts(x_signup.id)
            except RecursionError as e:
                await self.repo.block_email_confirm_by_email(x_signup.email)
                raise ErrExp(ExpCode.AUTH_MANY_CONFIRMATION_ATTEMPTS, str(e)) from e
            raise ErrExp(ExpCode.AUTH_WRONG_CODE)

        # TODO: Добавить сохранения записи в Account

        await self.repo.delete_email_signup(x_signup.id)
        return ZAccountID(id=x_signup.id)

    @staticmethod
    def _is_blocked(dt: datetime | None) -> bool:
        if not dt:
            return False
        return dt > datetime.now()
