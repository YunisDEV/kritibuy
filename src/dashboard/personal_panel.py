from ..db import session, User, Permission


def processPayments(payments, user):
    pms = []
    for payment in payments:
        pObj = {
            "id": None,
            "account": None,
            "amount": None,
            "date": None
        }
        if payment.fromUser == user.id:
            pTo = session.query(User).filter(User.id == payment.toUser).one()
            pToPermission = session.query(Permission).filter(
                Permission.id == pTo.permission).one()
            pObj["id"] = payment.id
            pObj["amount"] = float(payment.amount * -1)
            pObj["date"] = payment.createdAt.strftime('%d %b. %Y %H:%M')
            if pToPermission.name == 'Personal':
                pObj["account"] = pTo.fullName
            else:
                pObj["account"] = pTo.brandName

            pms.append(pObj)
        elif payment.toUser == user.id:
            pFrom = session.query(User).filter(
                User.id == payment.fromUser).one()
            pFromPermission = session.query(Permission).filter(
                Permission.id == pFrom.permission).one()
            pObj["id"] = payment.id
            pObj["amount"] = float(payment.amount)
            pObj["date"] = payment.createdAt.strftime('%d %b. %Y %H:%M')
            if pFromPermission.name == 'Personal':
                pObj["account"] = pFrom.fullName
            else:
                pObj["account"] = pFrom.brandName
            pms.append(pObj)
    return pms
