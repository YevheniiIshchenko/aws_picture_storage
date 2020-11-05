import psycopg2
import json

conn = psycopg2.connect(
    database="postgres",
    user="master",
    password="qaz123_zxc",
    host="database-1.c6my26cyocxp.us-east-1.rds.amazonaws.com",
    port='5432'
)

cursor = conn.cursor()

base_url = "https://yevhenii-aws-lambda-pictures.s3.amazonaws.com/"


def handler(event, context):

    key = event["Records"][0]['s3']['object']['key']
    email_name=key.split('_')
    email = email_name[0].replace('%40', '@')
    name = email_name[1]
    link = base_url+key

    req_text = f'''
        INSERT INTO users_pictures (email, picture_name, picture_link)
        VALUES ('{email}', '{name}', '{link}');
        '''

    cursor.execute(req_text)
    conn.commit()

    responseBody = event
    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(responseBody),
        "isBase64Encoded": False,
    }
    return response
