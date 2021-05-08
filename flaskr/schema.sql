-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS CombinedData;
DROP TABLE IF EXISTS Applicant;
DROP TABLE IF EXISTS OtherInformation;
DROP TABLE IF EXISTS Address;
DROP TABLE IF EXISTS Documents;
DROP TABLE IF EXISTS Program;
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE Applicant (
  applicantID INTEGER PRIMARY KEY AUTOINCREMENT,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  email TEXT NOT NULL,
  phone INTEGER NOT NULL,
  zipcode INTEGER NOT NULL,
  FOREIGN KEY (zipcode) REFERENCES Address (zipCode)
);

CREATE TABLE OtherInformation (
  InfoID INTEGER PRIMARY KEY AUTOINCREMENT,
  applicantID INTEGER NULL,
  documentID INTEGER NULL,
  programID INTEGER NULL,
  score INTEGER DEFAULT 100,
  decision TEXT DEFAULT "PASS",
  FOREIGN KEY (documentID) REFERENCES Documents (documentID),
  FOREIGN KEY (programID) REFERENCES Program (programID)
);

CREATE TABLE Address (
  AddressID INTEGER PRIMARY KEY AUTOINCREMENT,
  zipCode INTEGER NOT NULL,
  streetname TEXT NOT NULL,
  city TEXT NOT NULL,
  country TEXT NOT NULL
);

CREATE TABLE Documents (
  documentID INTEGER PRIMARY KEY AUTOINCREMENT,
  docDescription TEXT  NOT NULL,
  document VARBINARY  NOT NULL,
  passDescription TEXT  NOT NULL,
  passport VARBINARY  NOT NULL,
  validation BOOLEAN  NULL 
);

CREATE TABLE Program (
  programID INTEGER PRIMARY KEY AUTOINCREMENT,
  programName TEXT NOT NULL,
  status  TEXT NOT NULL
);
