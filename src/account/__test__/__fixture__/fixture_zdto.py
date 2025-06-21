from datetime import datetime, timedelta
from account.domain.dto import ZAccount, ZAccountID, ZBanned, ZIsBusy
from account.domain.models import AccRole

zaccount = ZAccount(
    id="6dda82b8-72dd-42f4-af43-8dedd2dc2520",
    email="test@example.com",
    pwd_hash="e1ee98334d5bfd0810fa6c03beef3cc3d05486a56c9d32e9b528d9af4477e3fa",
    salt="a9330649b51c9ed1d905fddeabd606f7",
    role=AccRole.USER,
    count_ads=0,
)

zaccountid = ZAccountID(id="6dda82b8-72dd-42f4-af43-8dedd2dc2520")

zbanned_true = ZBanned(
    account_id="6dda82b8-72dd-42f4-af43-8dedd2dc2520",
    is_banned=True,
    blocked_at=datetime.now(),
    blocked_to=datetime.now() + timedelta(days=1)
)

zisbusy = ZIsBusy(
    is_busy=True
)
