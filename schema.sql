CREATE TABLE Permissions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Countries(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    alpha2 VARCHAR(5) NOT NULL,
    alpha3 VARCHAR(5) NOT NULL,
    flag_path TEXT NOT NULL
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
    username VARCHAR(255) NOT NULL,
    email TEXT NOT NULL,
    permission INTEGER NOT NULL,
    full_name TEXT NULL,
    address TEXT NULL,
    phone TEXT NULL,
    country INTEGER NOT NULL,
    city INTEGER NOT NULL,
    brand_logo_path TEXT NULL,
    brand_name TEXT NULL,
    account_created_at DATETIME NOT NULL,
    brand_product_types TEXT NULL,
    active BOOLEAN NOT NULL,

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
    from_user INTEGER NOT NULL,
    to_user INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    
    CONSTRAINT payment_user
        FOREIGN KEY (from_user,to_user)
        REFERENCES Users(id,id)
);

CREATE TABLE Reports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reporter INTEGER NOT NULL,
    header TEXT NOT NULL,
    body TEXT NOT NULL,
    date DATETIME NOT NULL,
    
    CONSTRAINT report_reporter
        FOREIGN KEY (reporter)
        REFERENCES Users(id)
);

CREATE TABLE Messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_user INTEGER NOT NULL,
    to_user INTEGER NOT NULL,
    message INTEGER NOT NULL,
    date DATETIME NOT NULL,
    
    CONSTRAINT message_user
        FOREIGN KEY (from_user,to_user)
        REFERENCES Users(id)
);

CREATE TABLE Wallets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    balance FLOAT NOT NULL, -- DEFAULT 0.0
    owner INTEGER NOT NULL,
    
    CONSTRAINT wallet_user
        FOREIGN KEY (owner)
        REFERENCES Users(id)
);

CREATE TABLE Orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ordered_to INTEGER NOT NULL,
    ordered_by INTEGER NOT NULL,
    order_text TEXT NOT NULL,
    order_price FLOAT NOT NULL,
    paid BOOLEAN NOT NULL, -- DEFAULT FALSE
    
    CONSTRAINT order_user
        FOREIGN KEY (ordered_by,ordered_to)
        REFERENCES Users(id)
);

CREATE TABLE OrderRating(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value INTEGER NOT NULL,
    by_user INTEGER NOT NULL,
    to_user INTEGER NOT NULL,
    for_order INTEGER NOT NULL,    
    
    CONSTRAINT rating_order
        FOREIGN KEY (for_order)
        REFERENCES Orders(id)

    CONSTRAINT rating_user
        FOREIGN KEY (by_user,to_user)
        REFERENCES Users(id)
);