Database connection
connection = psycopg2.connect(
    host="localhost",
    database="phoenix_db",
    user="postgres",
    password="1234",
    port="5432"