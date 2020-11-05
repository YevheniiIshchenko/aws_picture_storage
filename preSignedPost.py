import boto3
import json
import string

from random import randint, choice
from botocore.client import Config


def gen_random_name():
    symb = string.ascii_letters + string.digits
    length = randint(5,20)
    res = ""
    for _ in range(length):
        res += choice(symb)
    res += '.png'
    return res


bucket_name = 'yevhenii-aws-lambda-pictures'
s3_client = boto3.client(
    's3',
    config=Config(signature_version='s3v4'),
)
s3_res = boto3.resource('s3')
bucket = s3_res.Bucket(bucket_name)


def handler(event, context):
    count = 0
    for _ in bucket.objects.all():
        count += 1

    print(event)
    user_email = event['requestContext']['authorizer']['claims']['email']

    key = user_email + '_'
    key += gen_random_name()

    # params = {
    #     "Bucket": bucket_name,
    #     "Key": key,
    #     'ACL': 'public-read',
    # }

    fields = {
        "acl": "public-read",
        "Content-Type": "image/png",
        }

    cond = [
        {"acl": "public-read"},
        ["content-length-range",  1, 1024*1024*30],
    ]

    # data = s3_client.generate_presigned_url('put_object', Params=params, HttpMethod="PUT")
    data = s3_client.generate_presigned_post(
         Bucket=bucket_name,
         Key=key,
         Fields=fields,
         Conditions=cond,
    )

    responseBody = {
        "count": count,
        "data": data,

    }

    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(responseBody),
        "isBase64Encoded": False,
    }

    return response
