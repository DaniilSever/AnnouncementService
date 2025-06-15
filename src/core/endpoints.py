class _EndpointsAUTH:
    """Эндпоинты Auth сервиса"""

    # AUTH_HEALTHCHECK = "/api/auth/healthcheck"

    AUTH_SIGNUP_EMAIL = "/api/auth/signup/email"
    AUTH_SIGNIN_EMAIL = "/api/auth/signin/email"
    AUTH_SIGNIN_EMAIL_FORM = "/api/auth/signin/email/form"
    AUTH_CONFIRM_EMAIL = "/api/auth/confirm/email"
    AUTH_REFRESH_TOKEN = "/api/auth/refresh/token"
    AUTH_REVOKE_TOKEN = "/api/auth/revoke/token"


class _EndpointsACCOUNT:
    """Эндпоинты Account сервиса"""

    # ACCOUNT_HEALTHCHECK = "/api/account/healthcheck"

    ACCOUNT_CURRENT = "/api/account/"
    ACCOUNT_GET_BY_ID = "/api/acccount/{acc_id}"
    ACCOUNT_GET_BY_EMAIL = "/api/account/{email}"
    ACCOUNT_COPY_FOR_SIGNUP = "/api/account/copy/signup"
    ACCOUNT_GET_ALL = "/api/accounts/"
    ACCOUNT_IS_EMAIL_BUSY = "/api/account/{email}/is_busy"
    ACCOUNT_SEND_COMPLAINT = "/api/account/{acc_id}/complaint"


class _EndpointsADS:
    """Эндпоинты ADS сервиса"""

    # ADS_HEALTHCHECK = "/api/ads/healthcheck"

    # --- Действия с объявлениями
    ADS_CREATE = "/api/ads/create"
    ADS_CHANGE = "/api/ads/{ads_id}/change"
    ADS_CHANGE_CATEGORY = "/api/ads/{ads_id}/change/category"
    ADS_DELETE = "/api/ads/delete/{ads_id}"
    ADS_GET_ALL = "/api/ads"
    ADS_GET_BY_ME = "/api/ads/me"
    ADS_GET_BY_ID = "/api/ads/ads"
    ADS_GET_BY_ACCOUNT = "/api/ads/author"
    ADS_GET_COUNT_ADS_BY_ACCOUNT = "/api/ads/count/author"
    ADS_SEND_COMPLAINT = "/api/ads/{ads_id}/complaint"

    # --- Действия с комментариями
    ADS_ADD_COMMENTARY = "/api/ads/{ads_id}/commentary"
    ADS_GET_COMMENTATIES = "/api/ads/{ads_id}/commentaries"
    ADS_ACTION_COMMENTARY = "/api/ads/{ads_id}/{comm_id}"
    ADS_ADD_COMPLAINT_COMMENTARY = "/api/ads/{ads_id}/{comm_id}/complaint"

class _EndpointsCompl:
    """Эндпоинты Compl сервиса"""

    # COMPL_HEALTHCHECK = "/api/compl/healthcheck"

    COMPL_ADD_COMPLAINT = "/api/compl/create"
    COMPL_GET_MY_COMPLAINTS = "/api/compl/me"
    COMPL_GET_MY_COMPLAINT = "/api/compl/me/{compl_id}"


class _EndpointsADM:
    """Админские эндпоинты"""

    # ADM_HEALTHCHECK = "/api/adm/healthcheck"

    # --- ADS
    ADM_DELETE_ADS = "/api/adm/delete/ads/{ads_id}"
    ADM_DELETE_COMMENTARY = "/api/adm/delete/commentary/{comm_id}"
    # ADM_WARNING_ACCOUNT = "/api/adm/warn/{acc_id}"

    # --- Account
    ADM_SET_ROLE_ACCOUNT = "/api/adm/account/{acc_id}/set/role"
    ADM_SET_BAN_ACCOUNT = "/api/adm/account/{acc_id}/set/ban"
    ADM_SET_UNBAN_ACCOUNT = "/api/adm/account/{acc_id}/set/unban"

    # --- Compl
    ADM_GET_COMPLAINTS = "/api/adm/complaint"
    ADM_GET_COMPLAINT_BY_ID = "/api/adm/complaint/{compl_id}"


class Endpoints(
    _EndpointsAUTH,
    _EndpointsACCOUNT,
    _EndpointsADS,
    _EndpointsCompl,
    _EndpointsADM,
):
    """Глобальные класс эндпоинтов"""
