from aiohttp import web

from src.web.handlers import (create_card_handler, get_user_profile_handler,
                              remove_card_like_handler, set_card_like_handler,
                              update_user_avatar_handler,
                              update_user_profile_handler, delete_card_handler, get_cards_handler)

routes = [
    web.get('/v1/{cohort_id}/users/me', get_user_profile_handler),
    web.patch('/v1/{cohort_id}/users/me', update_user_profile_handler),
    web.patch('/v1/{cohort_id}/users/me/avatar', update_user_avatar_handler),
    web.post('/v1/{cohort_id}/cards', create_card_handler),
    web.get('/v1/{cohort_id}/cards', get_cards_handler),
    web.delete('/v1/{cohort_id}/cards/{card_id}', delete_card_handler),
    web.put('/v1/{cohort_id}/cards/likes/{card_id}', set_card_like_handler),
    web.delete('/v1/{cohort_id}/cards/likes/{card_id}', remove_card_like_handler),
]