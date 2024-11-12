import psycopg2
from dotenv import load_dotenv
import os


# Database connection function (assuming you are using psycopg2)


def get_db_connection():
    load_dotenv()  # Load environment variables from .env
    print("HI")
    DATABASE_URL = os.getenv("DATABASE_URL")
    print("\n\nDATABASE_URL=", DATABASE_URL)
    conn = psycopg2.connect(DATABASE_URL)

    # conn = psycopg2.connect(
    #     host="localhost",
    #     database="vandycv_db",
    #     user="vandycv_user",
    #     password="securepassword"
    # )
    return conn
