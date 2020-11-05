import psycopg2

conn = psycopg2.connect(
    database="postgres",
    user="master",
    password="qaz123_zxc",
    host="database-1.c6my26cyocxp.us-east-1.rds.amazonaws.com",
    port='5432'
)

cursor = conn.cursor()

# req_text = f'''
#     INSERT INTO users_pictures (email, picture_name, picture_link)
#     VALUES ('keki4', 'creeper.png', 'https:/omazon.lox.ua');
#     '''

# cursor.execute(req_text)
conn.commit()


# cursor.execute('''
# CREATE TABLE users_pictures(
#    email varchar(64),
#    picture_name varchar(32),
#    picture_link varchar(128)
# );
# '''
# )
#
# conn.commit()

req_text = f'''
    SELECT picture_name, picture_link FROM users_pictures WHERE email='kekkekovich4@gmail.ua';
    '''

cursor.execute(req_text)

records = cursor.fetchall()

print(type(records[0]))
print(records)
