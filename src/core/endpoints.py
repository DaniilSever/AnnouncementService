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
    # ACCOUNT_CURRENT = "/api/account/current"
    ACCOUNT_GET_BY_ID = "/api/acccount/{acc_id}"
    ACCOUNT_GET_BY_EMAIL = "/api/account/{email}"
    ACCOUNT_COPY_FOR_SIGNUP = "/api/account/copy/signup"
    ACCOUNT_GET_ALL = "/api/account/"
    ACCOUNT_IS_EMAIL_BUSY = "/api/account/{email}/is_busy"
    # ACCOUNT_GET_WARNINGS = "/api/account/warning"
    # ACCOUNT_GET_WARNING_BY_ID = "/api/account/warning/{warn_id}"


class _EndpointsADS:
    """Эндпоинты ADS сервиса"""

    # ADS_HEALTHCHECK = "/api/ads/healthcheck"

    # --- Действия с объявлениями
    ADS_CREATE = "/api/ads/create"
    ADS_CHANGE = "/api/ads/change/{ads_id}"
    ADS_DELETE = "/api/ads/delete/{ads_id}"
    ADS_GET_ALL = "/api/ads"
    ADS_GET_BY_ME = "/api/ads/me"
    ADS_GET_BY_ID = "/api/ads/ads"
    ADS_GET_BY_ACCOUNT = "/api/ads/author"
    # ADS_ADD_COMPLAINT = "/api/ads/{ads_id}/complaint"

    # --- Действия с комментариями
    ADS_ADD_COMMENTARY = "/api/ads/{ads_id}/commentary"
    ADS_GET_COMMENTATIES = "/api/ads/{ads_id}"
    ADS_CHANGE_COMMENTARY = "/api/ads/{ads_id}/{comm_id}"
    ADS_DELETE_COMMENTARY = "/api/ads/{ads_id}/{comm_id}"
    ADS_ADD_COMPLAINT_COMMENTARY = "/api/ads/{ads_id}/{comm_id}/complaint"


class _EndpointsADM:
    """Админские эндпоинты"""

    ADM_HEALTHCHECK = "/api/adm/healthcheck"
    ADM_DELETE_ADS = "/api/adm/delete/ads/{ads_id}"
    ADM_DELETE_COMMENTARY = "/api/adm/delete/commentary/{comm_id}"
    ADM_BAN_ACCOUNT = "/api/adm/ban/{acc_id}"
    ADM_WARNING_ACCOUNT = "/api/adm/warn/{acc_id}"
    ADM_UNBAN_ACCOUNT = "/api/adm/unban/{acc_id}"
    ADM_SET_ADM = "/api/adm/setadm/{acc_id}"
    ADM_GET_COMPLAINTS = "/api/adm/complaint"
    ADM_GET_COMPLAINT_BY_ID = "/api/adm/complaint/{comp_id}"


class Endpoints(
    _EndpointsAUTH,
    _EndpointsACCOUNT,
    _EndpointsADS,
    _EndpointsADM,
):
    """Глобальные класс эндпоинтов"""
