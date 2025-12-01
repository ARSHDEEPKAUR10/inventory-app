import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))

    # ---- item_id from path /item/{id} ----
    path_params = event.get("pathParameters") or {}
    item_id = path_params.get("id")

    # ---- location_id from body, query, or top-level ----
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
        response = table.get_item(
            Key={"item_id": item_id, "location_id": location_id}
        )
        item = response.get("Item")

        if not item:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Item not found"})
            }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(item, default=str)
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
