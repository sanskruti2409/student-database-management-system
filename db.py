# ====================================================================
# Project: Student Database Management System
# File: db.py
# Description: Handles PostgreSQL database connections using psycopg2
# ====================================================================

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Database configuration settings
# Default values can be overridden via environment variables or a .env file
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "student_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")  # Replace with your PostgreSQL password if different

def get_db_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    RealDictCursor allows us to access columns by name (e.g., student['first_name']).
    """
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            cursor_factory=RealDictCursor
        )
        return connection
    except psycopg2.OperationalError as error:
        print(f"[Database Connection Error]: {error}")
        raise error
