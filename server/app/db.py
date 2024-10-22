import psycopg2

# Database connection function (assuming you are using psycopg2)
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="vandycv_db",
        user="vandycv_user",
        password="securepassword"
    )
    return conn