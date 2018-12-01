import base64
import json

def nlp_kbo_data(event, context):
    output = []

    for record in event['records']:
        print(record)
        payload = base64.b64decode(base64.b64decode(record['data'])).decode('utf-8')
        payload_obj = json.loads(payload)
        print(payload_obj)

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(json.dumps(payload_obj).encode('utf-8')).decode('utf-8')
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {'records': output}
