import base64
import boto3
from konlpy.tag import Twitter
import json

dynamodb = boto3.client('dynamodb', region_name='ap-northeast-2')
response = dynamodb.scan(
    TableName = 'kbo-data',
    FilterExpression = "dsrc = :Datasrc and :startDate < #dt and #dt <= :endDate",
    ExpressionAttributeNames = {
        "#dt": "date"
    },
    ExpressionAttributeValues = {
        ":Datasrc": {
            'S': 'twitter',
        },
        ":startDate": {
            'S': '2018-11-02 00:00:00'
        },
        ":endDate": {
            'S': '2018-11-13 00:00:00'
        }
        # ":startDate": {
        #     'S': '2018.11.02 00:00'
        # },
        # ":endDate": {
        #     'S': '2018.11.13 00:00'
        # }
    }
)
print(response['Count'])

kinesis = boto3.client('firehose', region_name='ap-northeast-2')
twitter = Twitter()
for idx in range(0, response['Count']):
    id = response['Items'][idx]['id']['S']
    date = response['Items'][idx]['date']['S']
    # gallery
    # title = response['Items'][idx]['title']['S']

    # twitter
    tweet = response['Items'][idx]['tweet']['S']

    # zumnews
    # title = response['Items'][idx]['title']['S']
    # content = response['Items'][idx]['content']['S']


    # nlped_title = twitter.nouns(title)
    # nlped_content = twitter.nouns(content)
    nlped_tweet = twitter.nouns(tweet)

    # nouns_list = "|".join(nlped_title)
    # nouns_content = "|".join(nlped_content)
    nouns_tweet = "|".join(nlped_tweet)

    data = {
        'recordId': id,
        'date': date,
        'tweet': nouns_tweet,
        # 'title': nouns_list,
        # 'content': nouns_content,
    }
    print(data)
    data = (json.dumps(data)).encode("utf-8")

    response_kinesis = kinesis.put_record(
        DeliveryStreamName = 'kbo_stream',
        Record = {
            'Data': base64.b64encode(data),
        }
    )
    print(response_kinesis)