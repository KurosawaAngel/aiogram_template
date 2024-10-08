from aiogram import F, Router
from aiogram.filters import MagicData

admin_router = Router(name=__name__)
admin_router.message.filter(MagicData(F.event_chat.id == F.config.admin_chat_id))
admin_router.callback_query.filter(MagicData(F.event_chat.id == F.config.admin_chat_id))
