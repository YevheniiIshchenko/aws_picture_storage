import json


def presignup(event, context):    
    return {
                "message": "pre-safe-lambda", 
                "body": json.dumps(event),
            }

