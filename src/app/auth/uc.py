from core.configs import AuthConfig
from core.security import create_confirm_code, create_password_hash
from domain.auth.dto import QEmailSignup
from domain.auth.dto import ZEmailSignup
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
        except RecursionError:
            x_signup: XEmailSignup = await self.repo.block_email_confirm_by_email(req.email)

        return ZEmailSignup.model_validate(x_signup.model_dump(mode="json"))
