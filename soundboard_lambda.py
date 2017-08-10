import boto3
import json
import logging
import os
# import slackweb

from base64 import b64decode
from urlparse import parse_qs

#setting up AWS services KMS, and IOT Client
kms = boto3.client('kms')
client = boto3.client('iot-data', region_name='us-west-2')

#decrypting the key passed thru the gateway from slack
encrypted_slackKey = os.environ['slackKey']
expected_token = boto3.client('kms').decrypt(CiphertextBlob=b64decode(encrypted_slackKey))['Plaintext']

#setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    params = parse_qs(event['body'])
    token = params['token'][0]
    if token != expected_token:
        logger.error("Request token (%s) does not match expected", token)
        return respond(Exception("Invalid request token"))

    user = params['user_name'][0]
    command = params['command'][0]
    channel = params['channel_name'][0]
    command_text = params['text'][0]
    response_url = params['response_url'][0]

    if channel == 'awsiot':
        response = client.publish(
            topic='$aws/thing/soundBoard/shadow/update',
            qos=1,
            payload=json.dumps({"state": {"desired": {"function": command_text,"count": ""}}})
        )
        return respond(None, "user = %s command = %s channel = %s command_text = %s response_url = %s" %
                       (user, command, channel, command_text, response_url))
    else:
        return respond(None, "user = %s command = %s channel = %s command_text = %s response_url = %s" %
                       (user, command, channel, command_text, response_url))