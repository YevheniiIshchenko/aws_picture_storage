import json


def hello(event, context):
    body = {
        "message": "You smell like teen spirit (PUDGE)))0)",
        "answer": event,
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

