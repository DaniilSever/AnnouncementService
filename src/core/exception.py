from .response import ErrDetail, ErrResp

class _AuthExpCode:
    AUTH_SINGUP_NOT_FOUND = "404", "Регистрация не найдена"
    AUTH_MANY_REGISTRATION_ATTEMPTS = "400", "Много попыток регистрации"
    AUTH_MANY_CONFIRMATION_ATTEMPTS = "400", "Много попыток подтверждения"
    AUTH_EMAIL_BLOCKED = "400", "Почта заборкипрванна, причина: множество попыток регистрации/подтверждения"
    AUTH_WRONG_CODE = "400", "Неверный код подтверждения"






class ExpCode(
    _AuthExpCode,
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
