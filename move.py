import json
import boto3


def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    body = json.loads(event['body'])

    # Perform game logic and generate a response based on the message received
    # For example, determine the next move and which player to send it to

    response = {
        'statusCode': 200,
        'body': json.dumps({'message': 'Your game move was processed.'})
    }

    # Send the response to the client associated with the connection ID
    send_message_to_client(connection_id, json.dumps(response))

    return response

def send_message_to_client(connection_id, message):
    client = boto3.client('apigatewaymanagementapi', endpoint_url='YOUR_API_ENDPOINT')
    client.post_to_connection(ConnectionId=connection_id, Data=message)
