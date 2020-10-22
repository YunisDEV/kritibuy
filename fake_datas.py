from src.db import Permission, session
# Creating Admin permission
admin = Permission(name="Admin")
session.add(admin)

# Creating Personal permission
personal = Permission(name="Personal")
session.add(personal)

# Creating Business permission
business = Permission(name="Business")
session.add(business)

session.commit()
