DROP DATABASE IF EXISTS company;
CREATE DATABASE company;
USE company;

-- Table 1: Departments
CREATE TABLE DEPARTMENT (
    Dnumber INT PRIMARY KEY,
    Dname VARCHAR(50) NOT NULL,
    mgr_ssn CHAR(9),
    mgr_start_date DATE
);

-- Table 2: Employees
CREATE TABLE EMPLOYEE (
    ssn CHAR(9) PRIMARY KEY,
    fname VARCHAR(30) NOT NULL,
    lname VARCHAR(30) NOT NULL,
    bdate DATE,
    address VARCHAR(100),
    gender CHAR(1),
    salary DECIMAL(10,2),
    Dno INT NOT NULL,
    CONSTRAINT fk_employee_department
        FOREIGN KEY (Dno)
        REFERENCES DEPARTMENT(Dnumber)
);

-- Table 3: Projects
CREATE TABLE PROJECT (
    Pnumber INT PRIMARY KEY,
    Pname VARCHAR(50) NOT NULL,
    Plocation VARCHAR(50),
    Dno INT NOT NULL,
    CONSTRAINT fk_project_department
        FOREIGN KEY (Dno)
        REFERENCES DEPARTMENT(Dnumber)
);

-- Add the manager relationship after EMPLOYEE exists
ALTER TABLE DEPARTMENT
ADD CONSTRAINT fk_department_manager
FOREIGN KEY (mgr_ssn)
REFERENCES EMPLOYEE(ssn);

