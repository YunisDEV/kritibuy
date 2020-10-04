CREATE TABLE Permissions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Countries(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    alpha2 VARCHAR(5) NOT NULL,
    alpha3 VARCHAR(5) NOT NULL,
    flagPath TEXT NOT NULL
);

CREATE TABLE Cities(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country INTEGER NOT NULL,

    CONSTRAINT city_country
        FOREIGN KEY (country)
        REFERENCES Countries(id)
);

CREATE TABLE Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    permission INTEGER NOT NULL,
    fullName TEXT NULL,
    address TEXT NULL,
    phone TEXT NULL,
    country INTEGER NOT NULL,
    city INTEGER NOT NULL,
    brandLogoPath TEXT NULL,
    brandName TEXT UNIQUE NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    brandProductTypes TEXT NULL,
    active BOOLEAN DEFAULT false NOT NULL,

    CONSTRAINT user_permission
        FOREIGN KEY (permission)
        REFERENCES Permissions(id)

    CONSTRAINT user_country
        FOREIGN KEY (country)
        REFERENCES Countries(id)

    CONSTRAINT user_city
        FOREIGN KEY (city)
        REFERENCES Cities(id)
);

CREATE TABLE AuthTokens(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    token TEXT NOT NULL
);

CREATE TABLE Blogs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    creator INTEGER NOT NULL,

    CONSTRAINT blog_creator
        FOREIGN KEY (creator)
        REFERENCES Users(id)
);

CREATE TABLE Payments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fromUser INTEGER NOT NULL,
    toUser INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    CONSTRAINT payment_user
        FOREIGN KEY (fromUser,toUser)
        REFERENCES Users(id,id)
);

CREATE TABLE Reports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reporter INTEGER NOT NULL,
    header TEXT NOT NULL,
    body TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    CONSTRAINT report_reporter
        FOREIGN KEY (reporter)
        REFERENCES Users(id)
);

CREATE TABLE Messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fromUser INTEGER NOT NULL,
    toUser INTEGER NOT NULL,
    message INTEGER NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    CONSTRAINT message_user
        FOREIGN KEY (fromUser,toUser)
        REFERENCES Users(id,id)
);

CREATE TABLE Wallets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    balance FLOAT DEFAULT 0.0 NOT NULL,
    owner INTEGER NOT NULL,
    
    CONSTRAINT wallet_user
        FOREIGN KEY (owner)
        REFERENCES Users(id)
);

CREATE TABLE Orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    orderedTo INTEGER NOT NULL,
    orderedBy INTEGER NOT NULL,
    orderText TEXT NOT NULL,
    orderPrice FLOAT NOT NULL,
    paid BOOLEAN DEFAULT false NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    CONSTRAINT order_user
        FOREIGN KEY (orderedBy,orderedTo)
        REFERENCES Users(id,id)
);

CREATE TABLE OrderRating(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value INTEGER NOT NULL,
    byUser INTEGER NOT NULL,
    toUser INTEGER NOT NULL,
    forOrder INTEGER NOT NULL, 
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,   
    
    CONSTRAINT rating_order
        FOREIGN KEY (forOrder)
        REFERENCES Orders(id)

    CONSTRAINT rating_user
        FOREIGN KEY (byUser,toUser)
        REFERENCES Users(id,id)
);