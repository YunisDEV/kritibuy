from ...db import *


def orders_get(user):
    orders = session.query(Order).filter(
        Order.orderedTo == user.id and
        user.permission == session.query(Permission).filter(
            Permission.name == "Business"
        ).one().id
    ).all()
    bonus = {
        'OrderedBy': {},
        'OrderedTo': {},
    }
    for order in orders:
        bonus["OrderedBy"][order.id] = session.query(User).filter(
            User.id == order.orderedBy
        ).one().username
        bonus["OrderedTo"][order.id] = session.query(User).filter(
            User.id == order.orderedTo
        ).one().username
    return {
        "body": orders,
        "bonus": bonus
    }
