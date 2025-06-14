from .response import ErrDetail, ErrResp

class __SysExpCode:
    SYS_INVALID_JWT_TOKEN = "500", "Неверный токен"
    SYS_INVALID_API_KEY = "500", "Неверный api ключ"
    SYS_UNAUTHORIZE = "503", "Не авторизирован"
class __AuthExpCode:
    AUTH_SINGUP_NOT_FOUND = "404", "Регистрация не найдена"
    AUTH_MANY_REGISTRATION_ATTEMPTS = "400", "Много попыток регистрации"
    AUTH_MANY_CONFIRMATION_ATTEMPTS = "400", "Много попыток подтверждения"
    AUTH_EMAIL_BLOCKED = "400", "Почта заборкипрванна, причина: множество попыток регистрации/подтверждения"
    AUTH_WRONG_CODE = "400", "Неверный код подтверждения"
    AUTH_SIGNIN_WRONG_PASSWORD = "400", "Неверный пароль"
    AUTH_INVALID_TOKEN_TYPE = "400", "Неверный тип токена"
    AUTH_REFRESH_TOKEN_NOT_FOUND = "404", "Токен не найден"
    AUTH_REVOKE_TOKEN_NOT_FOUND = "404", "Активные токены не найдены"

class __AccExpCode:
    ACC_ACCOUNT_NOT_FOUND = "404", "Аккаунт не найдет"
    ACC_EMAIL_IS_BUSY = "400", "Емайл занят"

class __AdsExpCode:
    ADS_FILTER_ERR = "400", "Неверный фильтр записей"
    ADS_NOT_FOUND = "404", "Объявление не найдено"
    ADS_COMMENTARY_NOT_FOUND = "404", "Комментарий не найден"


class ExpCode(
    __SysExpCode,
    __AuthExpCode,
    __AccExpCode,
    __AdsExpCode,
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
