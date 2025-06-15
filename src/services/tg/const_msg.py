
ban_mapping = {
    "week": "неделю",
    "month": "месяц",
    "month3": "3 месяца",
    "year": "год",
}

async def get_code_msg(email: str, code: int) -> str:
    msg = "Благодарим за регистрацию!"
    msg += f"\n\nEmail: {email}"
    msg += f"\nКод подтверждения: {code}"
    return msg

async def get_ads_warning_msg(ads_title: str, reason: str) -> str:
    msg = "⚠️######WARNING######"
    msg += f"\n\nУважаемый автор объявления {ads_title}"
    msg += "\n\nВаше объявление было удалено с общей доски, в связи с нарушением правил платформы"
    msg += f"\nПричина: {reason}"
    msg += "\n\nПросим исправить нарушение"
    return msg

async def get_acc_ban_warning_msg(email: str, ban_time: str, blocked_to: str,  reason: str) -> str:
    msg = "⚠️######WARNING######"
    msg += f"\n\nУважаемый, пользователь с почтной: {email}"
    if ban_time == "forever":
        msg += "\n\nВы были перманентно заблокированны"
    else:
        msg += f"\n\nВы были заблокированны на {ban_mapping.get(ban_time)}"
    msg += f"\nПричина: {reason}"
    msg += f"\nРазблокировка через: {blocked_to}"
    return msg

async def get_acc_unban_warning_msg(email: str) -> str:
    msg = "⚠️######WARNING######"
    msg += f"\n\nУважаемый, пользователь с почтной: {email}"
    msg += "\n\nВы были разблокированны"
    return msg
