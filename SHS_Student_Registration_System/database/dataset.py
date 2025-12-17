# database/dataset.py
# Sample dataset with SQL INSERT statements for all tables

import mysql.connector
from database.connect_database import get_connection_params

def insert_sample_data():
    """Insert sample data into all tables"""
    connection_params = get_connection_params()
    conn = mysql.connector.connect(**connection_params)
    cursor = conn.cursor()
    
    try:
        # ============================================
        # ACCOUNTS TABLE
        # ============================================
        # 6 Student accounts
        accounts_students = [
            ("A1", "student1", "password123", "What is your favorite color?", "Blue", "student"),
            ("A2", "student2", "password123", "What is your favorite food?", "Pizza", "student"),
            ("A3", "student3", "password123", "What is your favorite animal", "Dog", "student"),
            ("A4", "student4", "password123", "What is your favorite color?", "Red", "student"),
            ("A5", "student5", "password123", "What is your favorite food?", "Burger", "student"),
            ("A6", "student6", "password123", "What is your favorite animal", "Cat", "student"),
        ]
        
        # 3 Registrar accounts
        accounts_registrars = [
            ("A7", "registrar1", "password123", "What is your favorite color?", "Green", "registrar"),
            ("A8", "registrar2", "password123", "What is your favorite food?", "Pasta", "registrar"),
            ("A9", "registrar3", "password123", "What is your favorite animal", "Bird", "registrar"),
        ]
        
        # 1 Admin account
        accounts_admin = [
            ("A10", "admin1", "password123", "What is your favorite color?", "Purple", "admin"),
        ]
        
        all_accounts = accounts_students + accounts_registrars + accounts_admin
        
        cursor.executemany("""
            INSERT INTO accounts (AccountID, Username, Password, SecurityQuestion, SecurityAnswer, Role)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, all_accounts)
        
        print(f"✓ Inserted {len(all_accounts)} accounts")
        
        # ============================================
        # STUDENTS TABLE
        # ============================================
        students = [
            ("S1", "A1", "123456789012", "Juan", "Cruz", "Dela Cruz", "Male", "2008-05-15", 16, "Filipino", "Catholic", "Single", "09123456789", "juan.delacruz@email.com"),
            ("S2", "A2", "123456789013", "Maria", "Santos", "Garcia", "Female", "2008-08-20", 16, "Filipino", "Catholic", "Single", "09123456790", "maria.garcia@email.com"),
            ("S3", "A3", "123456789014", "Jose", "Reyes", "Lopez", "Male", "2007-12-10", 17, "Filipino", "Catholic", "Single", "09123456791", "jose.lopez@email.com"),
            ("S4", "A4", "123456789015", "Ana", "Villanueva", "Torres", "Female", "2008-03-25", 16, "Filipino", "Catholic", "Single", "09123456792", "ana.torres@email.com"),
            ("S5", "A5", "123456789016", "Carlos", "Fernandez", "Ramos", "Male", "2007-09-30", 17, "Filipino", "Catholic", "Single", "09123456793", "carlos.ramos@email.com"),
            ("S6", "A6", "123456789017", "Sofia", "Martinez", "Aquino", "Female", "2008-07-12", 16, "Filipino", "Catholic", "Single", "09123456794", "sofia.aquino@email.com"),
        ]
        
        cursor.executemany("""
            INSERT INTO students (StudentID, AccountID, LRN, FirstName, MiddleName, LastName, Gender, Birthdate, Age, Nationality, Religion, CivilStatus, ContactNum, Email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, students)
        
        print(f"✓ Inserted {len(students)} students")
        
        # ============================================
        # ADDRESS TABLE
        # ============================================
        addresses = [
            ("S1", "123", "Barangay 1", "Davao City", "Davao Del Sur", "8000"),
            ("S2", "456", "Barangay 2", "Davao City", "Davao Del Sur", "8000"),
            ("S3", "789", "Barangay 3", "Davao City", "Davao Del Sur", "8000"),
            ("S4", "321", "Barangay 4", "Davao City", "Davao Del Sur", "8000"),
            ("S5", "654", "Barangay 5", "Davao City", "Davao Del Sur", "8000"),
            ("S6", "987", "Barangay 6", "Davao City", "Davao Del Sur", "8000"),
        ]
        
        cursor.executemany("""
            INSERT INTO address (StudentID, HouseNum, Barangay, City, Province, ZIP)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, addresses)
        
        print(f"✓ Inserted {len(addresses)} addresses")
        
        # ============================================
        # ACADEMIC TABLE
        # ============================================
        academics = [
            ("S1", "Grade 11", "Academic", "STEM"),
            ("S2", "Grade 11", "Academic", "HUMSS"),
            ("S3", "Grade 12", "Academic", "ABM"),
            ("S4", "Grade 11", "TVL", "ICT"),
            ("S5", "Grade 12", "TVL", "HE"),
            ("S6", "Grade 11", "TVL", "IA"),
        ]
        
        cursor.executemany("""
            INSERT INTO academic (StudentID, GradeLevel, Track, Strand)
            VALUES (%s, %s, %s, %s)
        """, academics)
        
        print(f"✓ Inserted {len(academics)} academic records")
        
        # ============================================
        # PARENT/GUARDIAN TABLE
        # ============================================
        parent_guardians = [
            ("S1", "Pedro Dela Cruz", "Father", "Engineer", "123 Barangay 1, Davao City, Davao Del Sur, 8000", "09123456788"),
            ("S2", "Rosa Garcia", "Mother", "Teacher", "456 Barangay 2, Davao City, Davao Del Sur, 8000", "09123456789"),
            ("S3", "Miguel Lopez", "Father", "Doctor", "789 Barangay 3, Davao City, Davao Del Sur, 8000", "09123456790"),
            ("S4", "Carmen Torres", "Mother", "Nurse", "321 Barangay 4, Davao City, Davao Del Sur, 8000", "09123456791"),
            ("S5", "Roberto Ramos", "Father", "Lawyer", "654 Barangay 5, Davao City, Davao Del Sur, 8000", "09123456792"),
            ("S6", "Elena Aquino", "Mother", "Accountant", "987 Barangay 6, Davao City, Davao Del Sur, 8000", "09123456793"),
        ]
        
        cursor.executemany("""
            INSERT INTO parent_guardian (StudentID, Name, Relationship, Occupation, Address, ContactNum)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, parent_guardians)
        
        print(f"✓ Inserted {len(parent_guardians)} parent/guardian records")
        
        # ============================================
        # EMPLOYEE TABLE
        # ============================================
        employees = [
            ("E1", "A7", "Registrar One", "09123456795", "registrar1@school.edu"),
            ("E2", "A8", "Registrar Two", "09123456796", "registrar2@school.edu"),
            ("E3", "A9", "Registrar Three", "09123456797", "registrar3@school.edu"),
            ("E4", "A10", "Admin One", "09123456798", "admin1@school.edu"),
        ]
        
        cursor.executemany("""
            INSERT INTO employee (EmployeeID, AccountID, FullName, ContactNum, Email)
            VALUES (%s, %s, %s, %s, %s)
        """, employees)
        
        print(f"✓ Inserted {len(employees)} employees")
        
        # ============================================
        # REGISTRATION RECORD TABLE
        # ============================================
        registrations = [
            ("R1", "S1", "Grade 11", "Academic", "STEM", "2024-2025", "Pending", None),
            ("R2", "S2", "Grade 11", "Academic", "HUMSS", "2024-2025", "Approved", "E1"),
            ("R3", "S3", "Grade 12", "Academic", "ABM", "2024-2025", "Pending", None),
            ("R4", "S4", "Grade 11", "TVL", "ICT", "2024-2025", "Rejected", "E2"),
            ("R5", "S5", "Grade 12", "TVL", "HE", "2024-2025", "Approved", "E1"),
            ("R6", "S6", "Grade 11", "TVL", "IA", "2024-2025", "Pending", None),
        ]
        
        cursor.executemany("""
            INSERT INTO registration_record (RegistrationID, StudentID, GradeLevel, Track, Strand, SchoolYear, Status, ValidatedBy)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, registrations)
        
        print(f"✓ Inserted {len(registrations)} registration records")
        
        # ============================================
        # DOCUMENTS TABLE
        # ============================================
        documents = [
            ("D1", "S1", "R1", "Form 137", "/documents/S1/Form137.pdf"),
            ("D2", "S1", "R1", "Birth Certificate", "/documents/S1/BirthCertificate.pdf"),
            ("D3", "S1", "R1", "Report Card", "/documents/S1/ReportCard.pdf"),
            ("D4", "S1", "R1", "Good Moral", "/documents/S1/GoodMoral.pdf"),
            ("D5", "S2", "R2", "Form 137", "/documents/S2/Form137.pdf"),
            ("D6", "S2", "R2", "Birth Certificate", "/documents/S2/BirthCertificate.pdf"),
            ("D7", "S2", "R2", "Report Card", "/documents/S2/ReportCard.pdf"),
            ("D8", "S2", "R2", "Good Moral", "/documents/S2/GoodMoral.pdf"),
            ("D9", "S3", "R3", "Form 137", "/documents/S3/Form137.pdf"),
            ("D10", "S3", "R3", "Birth Certificate", "/documents/S3/BirthCertificate.pdf"),
            ("D11", "S4", "R4", "Form 137", "/documents/S4/Form137.pdf"),
            ("D12", "S4", "R4", "Birth Certificate", "/documents/S4/BirthCertificate.pdf"),
            ("D13", "S5", "R5", "Form 137", "/documents/S5/Form137.pdf"),
            ("D14", "S5", "R5", "Birth Certificate", "/documents/S5/BirthCertificate.pdf"),
            ("D15", "S5", "R5", "Report Card", "/documents/S5/ReportCard.pdf"),
            ("D16", "S5", "R5", "Good Moral", "/documents/S5/GoodMoral.pdf"),
            ("D17", "S6", "R6", "Form 137", "/documents/S6/Form137.pdf"),
            ("D18", "S6", "R6", "Birth Certificate", "/documents/S6/BirthCertificate.pdf"),
        ]
        
        cursor.executemany("""
            INSERT INTO documents (DocumentID, StudentID, RegistrationID, DocumentType, FilePath)
            VALUES (%s, %s, %s, %s, %s)
        """, documents)
        
        print(f"✓ Inserted {len(documents)} documents")
        
        # Commit all changes
        conn.commit()
        print("\n✓ All data inserted successfully!")
        
    except mysql.connector.Error as e:
        print(f"✗ Error inserting data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    insert_sample_data()

