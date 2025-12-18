# models/student_model.py
# Purpose: Model class for student-related database operations. Handles CRUD operations for students,
# addresses, academic records, and parent/guardian information. This follows OOP by encapsulating all
# student database logic in a single class, following the Model-View-Controller pattern.

import mysql.connector
from mysql.connector import Error
from database.connect_database import get_connection_params

# StudentModel class - OOP: Encapsulates student database operations
# This is an OOP class because it groups related database operations for students and their related data
# (address, academic, parent/guardian) into a cohesive unit. It follows encapsulation by providing a
# clean interface that hides database implementation details.
class StudentModel:
    def __init__(self, connection_params):
        self.conn_params = connection_params

    def create_connection(self):
        try:
            conn = mysql.connector.connect(**self.conn_params)
            return conn
        except Error as e:
            print(f"Database connection error: {e}")
            return None

    # Method: Generate a unique student ID with prefix S (S1, S2, etc.) by finding the highest existing ID
    def generate_student_id(self):
        conn = self.create_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        query = "SELECT StudentID FROM students WHERE StudentID LIKE 'S%' ORDER BY CAST(SUBSTRING(StudentID,2) AS UNSIGNED) DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            num = int(result[0][1:]) + 1
        else:
            num = 1
        return f"S{num}"

    # Method: Create a new student record along with related address, academic, and parent/guardian data
    # This method demonstrates OOP by grouping related operations (creating student and related records)
    # into a single method, ensuring data consistency through transaction handling.
    def create_student(self, account_id, lrn, first_name, middle_name, last_name, gender,
                       birthdate, age, nationality, religion, civil_status, contact_num, email,
                       address_data=None, academic_data=None, parent_data=None):
        conn = self.create_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        student_id = self.generate_student_id()

        try:
            # Insert into students table
            query_student = """
                INSERT INTO students
                (StudentID, AccountID, LRN, FirstName, MiddleName, LastName, Gender, Birthdate,
                 Age, Nationality, Religion, CivilStatus, ContactNum, Email)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(query_student, (
                student_id, account_id, lrn, first_name, middle_name, last_name, gender,
                birthdate, age, nationality, religion, civil_status, contact_num, email
            ))

            # Insert address
            if address_data:
                query_address = """
                    INSERT INTO address (StudentID, HouseNum, Barangay, City, Province, ZIP)
                    VALUES (%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(query_address, (
                    student_id,
                    address_data.get("HouseNum"),
                    address_data.get("Barangay"),
                    address_data.get("City"),
                    address_data.get("Province"),
                    address_data.get("ZIP")
                ))

            # Insert academic
            if academic_data:
                query_academic = """
                    INSERT INTO academic (StudentID, GradeLevel, Track, Strand)
                    VALUES (%s,%s,%s,%s)
                """
                cursor.execute(query_academic, (
                    student_id,
                    academic_data.get("GradeLevel"),
                    academic_data.get("Track"),
                    academic_data.get("Strand")
                ))

            # Insert parent/guardian
            if parent_data:
                query_parent = """
                    INSERT INTO parent_guardian (StudentID, Name, Relationship, Occupation, Address, ContactNum)
                    VALUES (%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(query_parent, (
                    student_id,
                    parent_data.get("Name"),
                    parent_data.get("Relationship"),
                    parent_data.get("Occupation"),
                    parent_data.get("Address"),
                    parent_data.get("ContactNum")
                ))

            conn.commit()
            return student_id

        except Error as e:
            print(f"Error creating student: {e}")
            return False

        finally:
            cursor.close()
            conn.close()

    # Method: Retrieve student information by account ID, including academic data via JOIN
    def get_student_by_account_id(self, account_id):
        conn = self.create_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT s.*, a.GradeLevel, a.Track, a.Strand
            FROM students s
            LEFT JOIN academic a ON s.StudentID = a.StudentID
            WHERE s.AccountID = %s
        """
        cursor.execute(query, (account_id,))
        student = cursor.fetchone()
        cursor.close()
        conn.close()
        return student

    # Method: Retrieve complete student data including address, academic, and parent/guardian information
    # This demonstrates OOP by providing a single method that aggregates related data from multiple tables
    def get_complete_student_data(self, student_id):
        conn = self.create_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT s.*, 
                   a.GradeLevel, a.Track, a.Strand,
                   ad.HouseNum, ad.Barangay, ad.City, ad.Province, ad.ZIP,
                   pg.Name as PGName, pg.Relationship, pg.Occupation, pg.Address as PGAddress, pg.ContactNum as PGContact
            FROM students s
            LEFT JOIN academic a ON s.StudentID = a.StudentID
            LEFT JOIN address ad ON s.StudentID = ad.StudentID
            LEFT JOIN parent_guardian pg ON s.StudentID = pg.StudentID
            WHERE s.StudentID = %s
        """
        cursor.execute(query, (student_id,))
        student = cursor.fetchone()
        cursor.close()
        conn.close()
        return student