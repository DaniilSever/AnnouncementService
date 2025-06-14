from datetime import datetime
from core.configs import AuthConfig
from core.security import create_confirm_code, create_password_hash, create_jwt_token, decode_jwt
from core.exception import ErrExp, ExpCode
from domain.auth.dto import QEmailSignup, QConfirmCode, QEmailSignin, QRefreshToken, QRevokeToken
from domain.auth.dto import ZEmailSignup, ZAccountID, ZToken, ZRevokedTokens
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

    async def signin_email(self, req: QEmailSignin) -> ZToken:

        # TODO: Добавить получение записи из Account

        pwd_hash, _ = create_password_hash(req.password, salt=z_acc.salt)
        if pwd_hash != z_acc.pwd_hash:
            raise ErrExp(ExpCode.AUTH_SIGNIN_WRONG_PASSWORD)
        
        access_payload = {
            "sub": str(z_acc.id),
            "type": "access",
        }
        access_token = create_jwt_token(access_payload, self.cfg.JWT_PRIVATE_KEY, delta=3600)

        refresh_payload = {
            "sub": str(z_acc.id),
            "type": "refresh",
        }
        refresh_token = create_jwt_token(refresh_payload, self.cfg.JWT_PRIVATE_KEY, delta=7 * 24 * 60 * 60)

        await self.repo.save_refresh_token(
            acc_id=z_acc.id,
            token=refresh_token,
        )
        return ZToken(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(self, req: QRefreshToken) -> ZToken:
        await self.repo.revoke_expired_tokens()

        payload = await decode_jwt(req.refresh_token, self.cfg.JWT_PUBLIC_KEY)
        if payload.get("type") != "refresh":
            raise ErrExp(ExpCode.AUTH_INVALID_TOKEN_TYPE)

        acc_id = payload["sub"]

        try:
            _ = await self.repo.get_refresh_token_for_account(acc_id, req.refresh_token)
        except KeyError as e:
            raise ErrExp(ExpCode.AUTH_REFRESH_TOKEN_NOT_FOUND, str(e)) from e

        access_payload = {
            "sub": str(acc_id)
        }
        access_token = create_jwt_token(access_payload, self.cfg.JWT_PRIVATE_KEY, delta=3600)

        return ZToken(access_token=access_token, refresh_token=req.refresh_token)

    async def revoke_token(self, req: QRevokeToken) -> ZRevokedTokens:
        count = await self.repo.revoke_tokens(acc_id=req.account_id)

        if count == 0:
            raise ErrExp(ExpCode.AUTH_REVOKE_TOKEN_NOT_FOUND)

        return ZRevokedTokens(
            message=f"Успешно отозван(ы) {count} токен(ы) "
        )


    # ------------------ Tools ------------------

    @staticmethod
    def _is_blocked(dt: datetime | None) -> bool:
        if not dt:
            return False
        return dt > datetime.now()
