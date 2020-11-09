import json

from db_connect import cursor


def handler(event, context) -> dict:

    email = event['requestContext']['authorizer']['claims']['email']

    req_text = f'''
    SELECT picture_name, picture_link FROM users_pictures WHERE email='{email}';
    '''

    cursor.execute(req_text)
    rec = cursor.fetchall()

    pictures = []

    for item in rec:
        # print(count, item)
        # print(count, type(item))
        name = item[0]
        link = item[1]
        pictures.append({
            "picture_name": name,
            "picture_link": link,
        })

    # print(event['requestContext']['authorizer']['claims'].keys())
    # print(event['requestContext']['authorizer']['claims'])

    print(pictures)

    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(pictures),
        "isBase64Encoded": False,
    }

    return response


