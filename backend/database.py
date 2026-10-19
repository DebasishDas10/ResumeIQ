
import pyodbc
import json

# SQL Server Configuration
SERVER = r"localhost\SQLEXPRESS"
DATABASE = "ResumeIQ"

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)


# Establish SQL Server Connection
def get_connection():
    return pyodbc.connect(CONNECTION_STRING, timeout=5)


# Save Resume Analysis Results
def save_analysis(filename, job_description, result):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
        INSERT INTO dbo.Resume_Analysis (
            File_Name,
            Job_Description,
            Match_Score,
            Matched_Skills,
            Missing_Skills,
            Total_Required_Skills,
            Total_Matched_Skills
        )
        OUTPUT INSERTED.Analysis_ID
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        values = (
            filename,
            job_description,
            result["match_score"],
            json.dumps(result["matched_skills"]),
            json.dumps(result["missing_skills"]),
            result["total_required_skills"],
            result["total_matched_skills"]
        )

        cursor.execute(query, values)

        analysis_id = cursor.fetchone()[0]

        connection.commit()

        return analysis_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# Retrieve Previous Resume Analysis Results
def get_analysis_history():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
        SELECT
            Analysis_ID,
            File_Name,
            Match_Score,
            Matched_Skills,
            Missing_Skills,
            Created_At
        FROM dbo.Resume_Analysis
        ORDER BY Analysis_ID DESC
        """

        cursor.execute(query)

        records = cursor.fetchall()

        history = []

        for record in records:

            history.append({
                "analysis_id": record.Analysis_ID,
                "filename": record.File_Name,
                "match_score": float(record.Match_Score),
                "matched_skills": json.loads(
                    record.Matched_Skills or "[]"
                ),
                "missing_skills": json.loads(
                    record.Missing_Skills or "[]"
                ),
                "created_at": (
                    record.Created_At.isoformat()
                    if record.Created_At
                    else None
                )
            })

        return history

    finally:
        connection.close()


# Test Database Connection
if __name__ == "__main__":

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT DB_NAME()")
        database_name = cursor.fetchone()[0]

        print("Connected to SQL Server successfully!")
        print("Connected Database:", database_name)

        connection.close()

    except pyodbc.Error as error:
        print("Database connection failed:")
        print(error)
