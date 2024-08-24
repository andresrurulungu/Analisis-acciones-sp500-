CREATE DATABASE  Proyecto;

USE Proyecto;

CREATE TABLE CompanyProfiles (
    Symbol VARCHAR(10) PRIMARY KEY ,  
    Company VARCHAR(100),            
    Sector VARCHAR(50),              
    Headquarters VARCHAR(100),       
    Fecha_fundada VARCHAR(50)  
);

CREATE TABLE Companies (
    Date DATE,
    Symbol VARCHAR(10),
    [Close] FLOAT,
    PRIMARY KEY (Date, Symbol),
    CONSTRAINT fk_Symbol FOREIGN KEY (Symbol) REFERENCES CompanyProfiles(Symbol)
);

