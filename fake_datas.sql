INSERT INTO Countries(name,alpha2,alpha3,flag_path)
VALUES 
('Azerbaijan','AZ','AZE','aze_flag.png'),
('Turkey','TR','TUR','tur_flag.png'),
('United States','US','USA','usa_flag.png');

INSERT INTO Cities(name,country)
VALUES
('Baku',(SELECT id from Countries WHERE name='Azerbaijan')),
('Ganja',(SELECT id from Countries WHERE name='Azerbaijan')),
('Istanbul',(SELECT id from Countries WHERE name='Turkey')),
('Ankara',(SELECT id from Countries WHERE name='Turkey')),
('San Francisco',(SELECT id from Countries WHERE name='United States')),
('Los Angeles',(SELECT id from Countries WHERE name='United States'));