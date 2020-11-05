import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid

USER_POOL_ID = 'us-east-1_m3djn2df2'
CLIENT_ID = '3644ops1enoprcv8dc8ipvt78b'
CLIENT_SECRET = '1ehv9b97199imosg512qoke2l4p4u938kv7p3nvdah96um653jhq'


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
        msg = str(msg).encode('utf-8'),   digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def signup(event, context):
    params = json.loads(event['body'])

    # if event["queryStringParameters"]:
    #   params = event.get("queryStringParameters")

    for field in ["email", "password"]:
        if not params.get(field):
            return {
                "error": False,
                "success": True,
                'message': f"{field} is not present",
                "data": None
            }
    email = params["email"]
    password = params['password']
    client = boto3.client('cognito-idp')
    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(email),
            Username=email,
            Password=password,
            UserAttributes=[
            {
                'Name': "email",
                'Value': email
            }
            ],
            ValidationData=[
                {
                'Name': "email",
                'Value': email
            },
            ])

    except client.exceptions.UsernameExistsException as e:
        return {"error": False,
               "success": True,
               "message": "This username already exists",
               "data": None}

    except client.exceptions.InvalidPasswordException as e:
        return {"error": False,
               "success": True,
               "message": "Password should have Caps,\
                          Special chars, Numbers",
               "data": None}

    except client.exceptions.UserLambdaValidationException as e:
        return {"error": False,
               "success": True,
               "message": "Email already exists",
               "data": None}

    except Exception as e:
        return {"error": False,
                "success": True,
                "message": str(e),
                "data": None}

    return {"error": False,
            "success": True,
            "message": "You are signed up! Your account is automatic confirmed",
            "data": None,
            }


def handler(event, context):
    responseBody = signup(event, context)
    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(responseBody),
        "isBase64Encoded": False
    }
    return response

