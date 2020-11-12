from ..db import session, Message, Order,  User, ServerError, Permission


def getCompany(comp_name):
    print('a')
    company = session.query(User).filter(
        User.brandName == comp_name
        and
        User.permission == session.query(Permission).filter(
            Permission.name == 'Business'
        ).one().id
    ).first()
    if not company:
        company = session.query(User).filter(
            User.brandNameSynonyms.any(comp_name)
            and
            User.permission == session.query(Permission).filter(
                Permission.name == 'Business'
            ).one().id
        ).first()
        if not company:
            raise Exception()

    return company
