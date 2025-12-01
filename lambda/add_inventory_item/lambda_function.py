import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))

    body_str = event.get("body")
    if not body_str:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing request body"})
        }

    try:
        body = json.loads(body_str)
    except Exception:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Body must be valid JSON"})
        }

    # Required fields
    required = [
        "item_id",
        "location_id",
        "item_name",
        "item_description",
        "qty_on_hand",
        "price"
    ]
    missing = [f for f in required if f not in body]
    if missing:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Missing fields: {', '.join(missing)}"})
        }

    try:
        item = {
            "item_id": str(body["item_id"]),
            "location_id": str(body["location_id"]),
            "item_name": str(body["item_name"]),
            "item_description": str(body["item_description"]),
            "qty_on_hand": int(body["qty_on_hand"]),
            "price": Decimal(str(body["price"]))  # avoid float
        }

        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(item, default=str)
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
