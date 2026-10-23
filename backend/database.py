
import os
import pyodbc
import json
import time
import logging

# ==========================================
# LOGGING CONFIGURATION
# ==========================================

logger = logging.getLogger(__name__)


# ==========================================
# SQL SERVER CONFIGURATION
# ==========================================

# Local SQL Server configuration
SERVER = r"localhost\SQLEXPRESS"
DATABASE = "ResumeIQ"

LOCAL_CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

# Azure SQL Database configuration
# Set DATABASE_CONNECTION_STRING in Azure App Service.
# If not configured, use local SQL Server.
CONNECTION_STRING = os.getenv(
    "DATABASE_CONNECTION_STRING",
    LOCAL_CONNECTION_STRING
)


# ==========================================
# ESTABLISH DATABASE CONNECTION
# WITH AUTOMATIC RETRY LOGIC
# ==========================================

def get_connection():

    max_attempts = 5

    retryable_errors = [
        "40613",  # Database temporarily unavailable
        "40197",  # Azure SQL service error
        "40501"   # Service busy
    ]

    for attempt in range(max_attempts):

        try:
            connection = pyodbc.connect(
                CONNECTION_STRING,
                timeout=30
            )

            return connection

        except pyodbc.Error as error:

            error_message = str(error)

            # Do not retry permanent or unknown errors
            if not any(
                code in error_message
                for code in retryable_errors
            ):
                logger.exception(
                    "Non-retryable database connection error"
                )
                raise

            # Stop after maximum attempts
            if attempt == max_attempts - 1:

                logger.exception(
                    "Database connection failed after %s attempts",
                    max_attempts
                )

                raise

            # Exponential backoff
            wait_seconds = min(
                2 ** (attempt + 1),
                15
            )

            logger.warning(
                "Azure SQL temporarily unavailable. "
                "Attempt %s/%s failed. "
                "Retrying in %s seconds.",
                attempt + 1,
                max_attempts,
                wait_seconds
            )

            time.sleep(wait_seconds)


# ==========================================
# SAVE RESUME ANALYSIS RESULTS
# ==========================================

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


# ==========================================
# RETRIEVE PREVIOUS ANALYSIS RESULTS
# ==========================================

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


# ==========================================
# TEST DATABASE CONNECTION
# ==========================================

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
