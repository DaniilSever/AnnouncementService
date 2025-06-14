from .response import ErrDetail, ErrResp

class _AuthExpCode:
    AUTH_SINGUP_NOT_FOUND = "404", "Регистрация не найдена"
    AUTH_MANY_REGISTRATION_ATTEMPTS = "400", "Много попыток регистрации"
    AUTH_MANY_CONFIRMATION_ATTEMPTS = "400", "Много попыток подтверждения"
    AUTH_EMAIL_BLOCKED = "400", "Почта заборкипрванна, причина: множество попыток регистрации/подтверждения"
    AUTH_WRONG_CODE = "400", "Неверный код подтверждения"
    AUTH_SIGNIN_WRONG_PASSWORD = "400", "Неверный пароль"
    AUTH_INVALID_TOKEN_TYPE = "400", "Неверный тип токена"
    AUTH_REFRESH_TOKEN_NOT_FOUND = "404", "Токен не найден"
    AUTH_REVOKE_TOKEN_NOT_FOUND = "404", "Активные токены не найдены"

class _AccExpCode:
    ACC_ACCOUNT_NOT_FOUND = "404", "Аккаунт не найдет"
    ACC_EMAIL_IS_BUSY = "400", "Емайл занят"




class ExpCode(
    _AuthExpCode,
    _AccExpCode,
):
    """Глобальные класс кодов ошибок"""




class ErrExp(Exception):
    """Базовое исключение для всех видов ошибок."""

    def __init__(self, code_msg: tuple, details: str | None = None):
        code, msg = code_msg
        self.status_code = code
        self.response = ErrResp(ok=False, err=ErrDetail(code=code, msg=msg, details=details))
        super().__init__(msg)

    def __repr__(self):
        return f"Error: {str(self.response.err)}"

    def __str__(self):
        return f"Error: {str(self.response.err)}"
