import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

INDEX_NAME = "Location-Index"

def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))

    # location_id from path, query, or top-level
    path_params = event.get("pathParameters") or {}
    location_id = path_params.get("location_id")

    if location_id is None:
        qs = event.get("queryStringParameters") or {}
        location_id = qs.get("location_id")

    if location_id is None:
        location_id = event.get("location_id")

    if not location_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "location_id is required"})
        }

    try:
        response = table.query(
            IndexName=INDEX_NAME,
            KeyConditionExpression=Key("location_id").eq(location_id)
        )
        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(items, default=str)
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
