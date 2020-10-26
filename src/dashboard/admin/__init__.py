from .get import *
from .update import *
from .post import *
from .delete import *


db_data_get = {
    "Permissions": permissions_get,
    "Countries": countries_get,
    "Cities": cities_get,
    "Users": users_get,
    "AuthTokens": authtokens_get,
    "Payments": payments_get,
    "Reports": reports_get,
    "Messages": messages_get,
    "Wallets": wallets_get,
    "OrderInfos": orderinfos_get,
    "Orders": orders_get,
    "OrderRatings": orderratings_get
}

db_data_post = {
    # "Permissions": permissions_post,
    "Countries": countries_post,
    "Cities": cities_post,
    # "Users": users_post,
    # "AuthTokens": authtokens_post,
    # "Payments": payments_post,
    # "Reports": reports_post,
    # "Messages": messages_post,
    # "Wallets": wallets_post,
    # "OrderInfos": orderinfos_post,
    # "Orders": orders_post,
    # "OrderRatings": orderratings_post
}

db_data_delete = {
    # "Permissions": permissions_delete,
    # "Countries": countries_delete,
    # "Cities": cities_delete,
    # "Users": users_delete,
    # "AuthTokens": authtokens_delete,
    # "Payments": payments_delete,
    # "Reports": reports_delete,
    # "Messages": messages_delete,
    # "Wallets": wallets_post,
    # "OrderInfos": orderinfos_delete,
    # "Orders": orders_delete,
    # "OrderRatings": orderratings_delete
}

db_data_update = {
    # "Permissions": permissions_update,
    # "Countries": countries_update,
    # "Cities": cities_update,
    # "Users": users_update,
    # "AuthTokens": authtokens_update,
    # "Payments": payments_update,
    # "Reports": reports_update,
    # "Messages": messages_update,
    # "Wallets": wallets_update,
    # "OrderInfos": orderinfos_update,
    # "Orders": orders_update,
    # "OrderRatings": orderratings_update
}
