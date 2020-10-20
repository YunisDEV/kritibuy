INSERT INTO Countries(name,alpha2,alpha3,flagPath)
VALUES 
('Azerbaijan','AZ','AZE','aze_flag.png'),
('Turkey','TR','TUR','tur_flag.png'),
('United States','US','USA','usa_flag.png');

INSERT INTO Cities(name,country)
VALUES
('Baku',(SELECT id from Countries WHERE name='Azerbaijan')),
('Ganja',(SELECT id from Countries WHERE name='Azerbaijan')),
('Sumgayit',(SELECT id from Countries WHERE name='Azerbaijan')),
('Guba',(SELECT id from Countries WHERE name='Azerbaijan')),
('Gabala',(SELECT id from Countries WHERE name='Azerbaijan')),
('Istanbul',(SELECT id from Countries WHERE name='Turkey')),
('Ankara',(SELECT id from Countries WHERE name='Turkey')),
('San Francisco',(SELECT id from Countries WHERE name='United States')),
('Washington D.C.',(SELECT id from Countries WHERE name='United States')),
('New York City',(SELECT id from Countries WHERE name='United States')),
('San Jose',(SELECT id from Countries WHERE name='United States')),
('Los Angeles',(SELECT id from Countries WHERE name='United States'));

INSERT INTO Permissions(name)
VALUES
('Admin'),
('Business'),
('Personal');

INSERT INTO Users(
    username,
    password,
    email,
    permission,
    country,
    city,
    active,
    confirmed)
VALUES
(
    'admin',
    '$2b$12$SsmnopkAVDZI/7QQjXa6XeoW6p8IqzI3OUsJyWEOVn0Tw23U7YbYm',
    'admin@kritibuy.com',
    (SELECT id FROM Permissions WHERE name='Admin'),
    (SELECT id FROM Countries WHERE name='Azerbaijan'),
    (SELECT id FROM Cities WHERE name='Baku'),
    true,
    true
)