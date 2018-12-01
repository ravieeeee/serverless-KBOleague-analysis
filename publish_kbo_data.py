import base64
import boto3
from konlpy.tag import Kkma
import json

dynamodb = boto3.client('dynamodb', region_name='ap-northeast-2')
response = dynamodb.scan(
    TableName = 'kbo-data',
    FilterExpression = "dsrc = :testsrc and #dt <= :dt",
    ExpressionAttributeNames = {
        "#dt": "date"
    },
    ExpressionAttributeValues = {
        ":testsrc": {
            'S': 'doosangallery',
        },
        ":dt": {
            'S': '2018-11-03 00:00:00'
        }
    }
)
print(response['Count'])

kinesis = boto3.client('firehose', region_name='ap-northeast-2')
kkma = Kkma()
for idx in range(0, response['Count']):
    id = response['Items'][idx]['id']['S']
    title = response['Items'][idx]['title']['S']
    date = response['Items'][idx]['date']['S']

    nlped_title = kkma.nouns(title)
    nouns_list = "|".join(nlped_title)

    data = {
        'recordId': id,
        'date': date,
        'title': nouns_list,
    }
    data = (json.dumps(data)).encode("utf-8")
    print(data)
    
    response_kinesis = kinesis.put_record(
        DeliveryStreamName = 'kbo_stream',
        Record = {
            'Data': base64.b64encode(data),
        }
    )
    print(response_kinesis)