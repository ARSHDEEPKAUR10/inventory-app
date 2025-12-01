import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))

    # item_id
    path_params = event.get("pathParameters") or {}
    item_id = path_params.get("id")

    # location_id
    location_id = None
    body_str = event.get("body")
    if body_str:
        try:
            body = json.loads(body_str)
            location_id = body.get("location_id")
        except Exception:
            pass

    if location_id is None:
        qs = event.get("queryStringParameters") or {}
        location_id = qs.get("location_id")

    if location_id is None:
        location_id = event.get("location_id")

    if not item_id or not location_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "item_id and location_id are required"})
        }

    try:
        table.delete_item(
            Key={"item_id": item_id, "location_id": location_id}
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Item deleted",
                "item_id": item_id,
                "location_id": location_id
            })
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
