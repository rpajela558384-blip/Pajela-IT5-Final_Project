# database/setup_database.py

import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )

def create_database(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS shs_registration_system")
    cursor.execute("USE shs_registration_system")

def create_tables(cursor):

    # ---------------------------
    # ACCOUNTS (ROOT TABLE)
    # ---------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            AccountID VARCHAR(16) PRIMARY KEY,
            Username VARCHAR(50) UNIQUE NOT NULL,
            Password VARCHAR(255) NOT NULL,
            SecurityQuestion VARCHAR(100),
            SecurityAnswer VARCHAR(100),
            Role ENUM('student','registrar','admin') NOT NULL
        ) ENGINE=InnoDB;
    """)

    # ---------------------------
    # STUDENTS
    # ---------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            StudentID VARCHAR(16) PRIMARY KEY,
            AccountID VARCHAR(16) NOT NULL,
            LRN VARCHAR(12) UNIQUE,
            FirstName VARCHAR(50),
            MiddleName VARCHAR(50),
            LastName VARCHAR(50),
            Gender ENUM('Male', 'Female'),
            Birthdate DATE,
            Age INT,
            Nationality VARCHAR(50),
            Religion VARCHAR(50),
            CivilStatus VARCHAR(20),
            ContactNum VARCHAR(20),
            Email VARCHAR(100),

            CONSTRAINT fk_students_account
                FOREIGN KEY (AccountID)
                REFERENCES accounts(AccountID)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        ) ENGINE=InnoDB;
    """)

    # ---------------------------
    # ADDRESS
    # ---------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS address (
            StudentID VARCHAR(16) PRIMARY KEY,
            HouseNum VARCHAR(50),
            Barangay VARCHAR(100),
            City VARCHAR(100),
            Province VARCHAR(100),
            ZIP VARCHAR(10),

            CONSTRAINT fk_address_student
                FOREIGN KEY (StudentID)
                REFERENCES students(StudentID)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        ) ENGINE=InnoDB;
    """)

    # ---------------------------
    # ACADEMIC
    # ---------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS academic (
            StudentID VARCHAR(16) PRIMARY KEY,
            GradeLevel ENUM('Grade 11', 'Grade 12'),
            Track ENUM('Academic', 'TVL'),
            Strand ENUM('STEM','HUMSS','ABM','ICT','HE','IA','GAS'),

            CONSTRAINT fk_academic_student
                FOREIGN KEY (StudentID)
                REFERENCES students(StudentID)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        ) ENGINE=InnoDB;
    """)

    # ---------------------------
    # PARENT / GUARDIAN
    # ---------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parent_guardian (
            StudentID VARCHAR(16) PRIMARY KEY,
            Name VARCHAR(100),
            Relationship VARCHAR(50),
            Occupation VARCHAR(100),
            Address VARCHAR(200),
            ContactNum VARCHAR(20),

            CONSTRAINT fk_parent_student
                FOREIGN KEY (StudentID)
                REFERENCES students(StudentID)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        ) ENGINE=InnoDB;
    """)

    # ---------------------------
    # EMPLOYEE
    # ---------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            EmployeeID VARCHAR(16) PRIMARY KEY,
            AccountID VARCHAR(16) UNIQUE,
            FullName VARCHAR(100),
            ContactNum VARCHAR(20),
            Email VARCHAR(100),

            CONSTRAINT fk_employee_account
                FOREIGN KEY (AccountID)
                REFERENCES accounts(AccountID)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        ) ENGINE=InnoDB;
    """)

    # ---------------------------
    # REGISTRATION RECORD
    # ---------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registration_record (
            RegistrationID VARCHAR(16) PRIMARY KEY,
            StudentID VARCHAR(16) NOT NULL,
            GradeLevel ENUM('Grade 11', 'Grade 12'),
            Track ENUM('Academic','TVL'),
            Strand ENUM('STEM','HUMSS','ABM','ICT','HE','IA','GAS'),
            SchoolYear VARCHAR(20),
            Status ENUM('Pending','Approved','Rejected') DEFAULT 'Pending',
            SubmittedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
            ValidatedBy VARCHAR(16) NULL,

            CONSTRAINT fk_registration_student
                FOREIGN KEY (StudentID)
                REFERENCES students(StudentID)
                ON DELETE CASCADE
                ON UPDATE CASCADE,

            CONSTRAINT fk_registration_employee
                FOREIGN KEY (ValidatedBy)
                REFERENCES employee(EmployeeID)
                ON DELETE SET NULL
                ON UPDATE CASCADE
        ) ENGINE=InnoDB;
    """)

    # ---------------------------
    # DOCUMENTS
    # ---------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            DocumentID VARCHAR(16) PRIMARY KEY,
            StudentID VARCHAR(16),
            RegistrationID VARCHAR(16),
            DocumentType VARCHAR(50),
            FilePath VARCHAR(255),

            CONSTRAINT fk_documents_student
                FOREIGN KEY (StudentID)
                REFERENCES students(StudentID)
                ON DELETE CASCADE
                ON UPDATE CASCADE,

            CONSTRAINT fk_documents_registration
                FOREIGN KEY (RegistrationID)
                REFERENCES registration_record(RegistrationID)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        ) ENGINE=InnoDB;
    """)


def main():
    conn = create_connection()
    cursor = conn.cursor()
    create_database(cursor)
    create_tables(cursor)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database and tables created successfully.")

if __name__ == "__main__":
    main()
