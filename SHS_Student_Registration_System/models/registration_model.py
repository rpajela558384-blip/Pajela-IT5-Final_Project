# models/registration_model.py

import mysql.connector
from mysql.connector import Error
from database.connect_database import get_connection_params

class RegistrationModel:
    def __init__(self, connection_params):
        self.conn_params = connection_params

    def create_connection(self):
        try:
            conn = mysql.connector.connect(**self.conn_params)
            return conn
        except Error as e:
            print(f"Database connection error: {e}")
            return None

    def generate_registration_id(self):
        """Generates a simple RegistrationID with prefix R (R1, R2, etc.)"""
        conn = self.create_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        query = "SELECT RegistrationID FROM registration_record WHERE RegistrationID LIKE 'R%' ORDER BY CAST(SUBSTRING(RegistrationID,2) AS UNSIGNED) DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            num = int(result[0][1:]) + 1
        else:
            num = 1
        return f"R{num}"

    def create_registration(self, student_id, grade_level, track, strand, school_year, documents=None):
        """
        Inserts a new registration record and optionally associated documents.
        documents: list of dicts [{DocumentType: str, FilePath: str}, ...]
        """
        conn = self.create_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        registration_id = self.generate_registration_id()

        try:
            # Insert registration record
            query_reg = """
                INSERT INTO registration_record
                (RegistrationID, StudentID, GradeLevel, Track, Strand, SchoolYear)
                VALUES (%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(query_reg, (registration_id, student_id, grade_level, track, strand, school_year))

            # Insert documents
            if documents:
                query_doc = """
                    INSERT INTO documents (DocumentID, StudentID, RegistrationID, DocumentType, FilePath)
                    VALUES (%s,%s,%s,%s,%s)
                """
                for doc in documents:
                    # Generate sequential DocumentID
                    cursor.execute(
                        "SELECT DocumentID FROM documents WHERE DocumentID LIKE 'D%' ORDER BY CAST(SUBSTRING(DocumentID,2) AS UNSIGNED) DESC LIMIT 1")
                    result = cursor.fetchone()
                    if result:
                        num = int(result[0][1:]) + 1
                    else:
                        num = 1
                    doc_id = f"D{num}"
                    cursor.execute(query_doc,
                                   (doc_id, student_id, registration_id, doc["DocumentType"], doc["FilePath"]))

            conn.commit()
            return registration_id

        except Error as e:
            print(f"Error creating registration: {e}")
            return False

        finally:
            cursor.close()
            conn.close()

    def get_registration_by_student(self, student_id):
        """Fetches all registration records for a student with associated documents"""
        conn = self.create_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT rr.*, d.DocumentID, d.DocumentType, d.FilePath
            FROM registration_record rr
            LEFT JOIN documents d ON rr.RegistrationID = d.RegistrationID
            WHERE rr.StudentID = %s
        """
        cursor.execute(query, (student_id,))
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records

    def update_status(self, registration_id, status, validated_by=None):
        """Updates the registration status and who validated it"""
        conn = self.create_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        try:
            query = "UPDATE registration_record SET Status = %s, ValidatedBy = %s WHERE RegistrationID = %s"
            cursor.execute(query, (status, validated_by, registration_id))
            conn.commit()
            return True
        except Error as e:
            print(f"Error updating registration status: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def get_monthly_registrations(self, year=None):
        """Get monthly registration counts for a given year (or current year if not specified)"""
        conn = self.create_connection()
        if not conn:
            return []
        cursor = conn.cursor(dictionary=True)
        
        if year is None:
            from datetime import datetime
            year = datetime.now().year
        
        query = """
            SELECT 
                MONTH(SubmittedAt) as month,
                COUNT(*) as count
            FROM registration_record
            WHERE YEAR(SubmittedAt) = %s
            GROUP BY MONTH(SubmittedAt)
            ORDER BY month
        """
        cursor.execute(query, (year,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
