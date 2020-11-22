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

def invoice_get(order_id):
    order_info = {}
    order = session.query(Order).filter(Order.id == order_id).one()
    ordered_by = session.query(User).filter(
        User.id == order.orderedBy).one()
    order_info = {
        "Order": {
            "ID": order.id,
            "Message": order.orderText,
            "Product": order.orderedProduct,
            "Date": order.createdAt.strftime('%d %b. %Y %H:%M'),
        },
        "Customer": {
            "Username": ordered_by.username,
            "Full name": ordered_by.fullName,
            "E-mail": ordered_by.email,
            "Address": ordered_by.address,
            "Phone number": ordered_by.phone,
            "Country": session.query(Country).filter(Country.id == ordered_by.country).one().name,
            "City": session.query(City).filter(City.id == ordered_by.city).one().name
        }
    }
    return order_info