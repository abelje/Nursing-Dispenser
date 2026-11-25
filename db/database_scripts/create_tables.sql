--create tables

CREATE TABLE IF NOT EXISTS user(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    inserted_on TEXT DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS patient(
    ID INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_patient (
    user_id INTEGER,
    patient_id INTEGER,

    PRIMARY KEY (user_id, patient_id),

    FOREIGN KEY (user_id)
        REFERENCES user(ID),
    FOREIGN KEY (patient_id)
        REFERENCES patient(ID)
);

CREATE TABLE IF NOT EXISTS drug(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    drawer_num INTEGER NOT NULL,
    dosage INTEGER NOT NULL,
    route TEXT NOT NULL,
    start_hour INTEGER NOT NULL,
    current_hour INTEGER NOT NULL,
    frequency INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS patient_drug(
    patient_id INTEGER,
    drug_id INTEGER,

    PRIMARY KEY (patient_id, drug_id),

    FOREIGN KEY (patient_id)
        REFERENCES patient(ID)
    FOREIGN KEY (drug_id)
        REFERENCES drug(ID)
);

-- insert values into them

INSERT INTO user (username, password, inserted_on, last_login)
VALUES
('Herald', '123$$321', '10-12-2026', NULL),
('Joseph', 'Jesus4U', '8-2-2025', NULL),
('Stephanie', 'BadBoss', '5-21-2021', NULL),
('Carolyn', 'Work4ever!', '12-12-2012', NULL);

--UPDATE user

INSERT INTO patient (ID, first_name, last_name, date_of_birth)
VALUES
(111, 'Jacob', 'Wonderful', '1988-06-22'),
(112, 'Mary', 'Peterson', '1960-02-01'),
(113, 'Nathan', 'Brown', '2002-12-12'),
(114, 'Joanna', 'Tobias', '1995-03-26'),
(115, 'Emily', 'Johnson', '1995-04-18'),
(116, 'Michael', 'Smith', '1978-09-25'),
(117, 'Sarah', 'Williams', '1989-11-03'),
(118, 'David', 'Jones', '1965-07-14'),
(119, 'Olivia', 'Davis', '2001-01-29'),
(120, 'James', 'Miller', '1982-03-08'),
(121, 'Sophia', 'Wilson', '1998-12-17'),
(122, 'Daniel', 'Moore', '1972-05-21'),
(123, 'Emma', 'Taylor', '2005-08-11'),
(124, 'William', 'Anderson', '1959-10-06'),
(125, 'Ava', 'Thomas', '1993-02-14');

INSERT INTO user_patient (user_id, patient_id)
VALUES
(1, 115),
(1, 117),
(1, 118),
(1, 119),
(1, 124),
(1, 125),
(1, 111),
(1, 113),
(3, 112);

INSERT INTO drug (name, drawer_num, dosage, route, start_hour, current_hour, frequency)
VALUES
('drug A', 1, 2, 'mouth', 12, 9, 3),
('drug B', 2, 2, 'mouth', 10, 9, 1);

INSERT INTO patient_drug (patient_id, drug_id)
VALUES
(111, 1),
(111, 2),
(113, 1),
(112, 1),
(112, 4);