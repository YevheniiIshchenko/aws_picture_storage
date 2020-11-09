import psycopg2

conn = psycopg2.connect(
    database="postgres",
    user="master",
    password="qaz123_zxc",
    host="database-1.c6my26cyocxp.us-east-1.rds.amazonaws.com",
    port='5432'
)

cursor = conn.cursor()


