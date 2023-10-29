import json

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    
    # You can add additional logic for handling $disconnect, if needed
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Disconnected successfully!'})
    }
