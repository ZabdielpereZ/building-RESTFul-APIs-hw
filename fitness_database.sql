-- CREATING fitness database

CREATE DATABASE fitness;

USE fitness; -- Telling my interpreter which database to use for this script file

-- Creating Members Table
CREATE TABLE members 
( id INT AUTO_INCREMENT PRIMARY KEY,
members_name VARCHAR(75) NOT NULL,
email VARCHAR(150) NULL,
phone CHAR(16) NULL
);

-- Creating Sessions Table
CREATE TABLE workout_sessions
( id INT AUTO_INCREMENT PRIMARY KEY,
duration TIME ,
members_id INT,
FOREIGN KEY (members_id) REFERENCES members(id)
);

-- Altering Tabels by adding members
INSERT INTO members (members_name, email, phone) VALUES
('Mozinni', 'poptart@mail.milk', '1594563586'),
('Zab', 'look@menow.mail', '6524857545'), 
('Ruppee', 'meow@meow.meow', '3621520145'), 
('Lisa J Simpson', 'rules@rule.wow', '5036295864'),
('Bart J Simpson', 'yousmell@aye.cramba', '5035625414');


-- Viewing our Tables
SELECT * FROM members;
SELECT * FROM workout_sessions;

-- DELETING TABLES
DROP TABLE members;
DROP TABLE workout_sessions;