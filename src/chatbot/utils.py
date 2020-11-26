from ..db import session, User, Permission
from sqlalchemy import func

def getCompany(comp_name):
    company = session.query(User).filter(
        func.lower(User.brandName) == func.lower(comp_name)
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
