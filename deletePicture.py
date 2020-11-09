import boto3
import json

from db_connect import conn, cursor

s3 = boto3.resource('s3')
bucket_name = 'yevhenii-aws-lambda-pictures'


def delete(event, context) -> str:
    email = event['requestContext']['authorizer']['claims']['email']

    params = json.loads(event['body'])
    if not params.get('key') :
        return 'Key is absent!'
    key=params['key']
    key_s3 = email+'_'+key

    # Looking for picture

    req_text = f'''
    SELECT * FROM users_pictures WHERE email='{email}' AND picture_name='{key}';
    '''
    cursor.execute(req_text)
    rec = cursor.fetchall()
    if len(rec) == 0:
        return 'There is no picture with this name!'

    # Deleting
    req_text = f'''
    DELETE FROM users_pictures WHERE email='{email}' AND picture_name='{key}';
    '''
    cursor.execute(req_text)
    conn.commit()
    s3.Object(bucket_name, key_s3).delete()

    return "Picture was successfully deleted!"


def handler(event, context):
    message = delete(event, context)

    responseBody = {
        'message': message,
    }

    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(responseBody),
        "isBase64Encoded": False,
    }
    return response

