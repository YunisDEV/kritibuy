from src.db import (
    session,
    Permission,
    Country,
    City,
    User,
    Wallet
)

# Creating Permissions
permissions = ['Admin', 'Personal', 'Business']

for i in permissions:
    session.add(Permission(name=i))
session.commit()
# Creating Countries
countries = {
    "Azerbaijan": ['AZ', 'AZE', '/countryflags/aze_flag.png'],
    "Turkey": ['TR', 'TUR', '/countryflags/tur_flag.png'],
    "United States": ['US', 'USA', '/countryflags/usa_flag.png']
}

for i in countries.items():
    session.add(Country(
        name=i[0],
        alpha2=i[1][0],
        alpha3=i[1][1],
        flagPath=i[1][2],
    ))
session.commit()
# Creating Cities
cities = {
    "Baku": "Azerbaijan",
    "Ganja": "Azerbaijan",
    "Sumgayit": "Azerbaijan",
    "Guba": "Azerbaijan",
    "Gabala": "Azerbaijan",
    "Istanbul": "Turkey",
    "Ankara": "Turkey",
    "Trabzon": "Turkey",
    "San Francisco": "United States",
    "Washington D.C.": "United States",
    "San Jose": "United States",
    "Los Angeles": "United States"
}

for i in cities.items():
    session.add(City(
        name=i[0],
        country=session.query(Country).filter(Country.name == i[1]).one().id
    ))
session.commit()
adminProfile = User(
    username='admin',
    password='Admin123',
    email='admin@kritibuy.com',
    permission=session.query(Permission).filter(
        Permission.name == 'Admin'
    ).one().id,
    country=session.query(Country).filter(
        Country.name == 'Azerbaijan'
    ).one().id,
    city=session.query(City).filter(
        City.name == 'Baku'
    ).one().id,
    active=True,
    confirmed=True
)

session.add(adminProfile)
session.commit()

session.add(Wallet(
    owner=adminProfile.id
))

session.commit()
