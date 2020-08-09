import boto3
import sys
import json
import random

client = boto3.client('sns')

def load_monkeys(template):
    if template['CCSTemplateFormatVersion']:
        print(template['CCSTemplateFormatVersion'])
        if template['CCSEvents']:
            global fields, target, value, subject, message
            fields = template['CCSEvents']
            keys = list(fields.keys())
            r = random.randrange(len(keys))
            target = keys[r]
            ccsevent = fields[target]
            if 'Values' in ccsevent:
                r = random.randrange(len(ccsevent['Values']))
                value = ccsevent['Values'][random.randrange(len(ccsevent['Values']))]
            else:
                value =  target + ' deleted'
            scenario = ccsevent['Events'][random.randrange(len(ccsevent['Events']))]
            subjects = template['CCSMessages'][scenario]['Subjects']
            subject = subjects[random.randrange(len(subjects))]
            messages = template['CCSMessages'][scenario]['Messages']
            message = messages[random.randrange(len(messages))]
            if 'Outputs' not in template:
                 template['Outputs'] = {}
            template['Outputs']['CloudChaosScenario'] = {} 
            template['Outputs']['CloudChaosScenario']['Value'] = scenario
            template['Outputs']['CloudChaosSubject'] = {} 
            template['Outputs']['CloudChaosSubject']['Value'] = subject
            template['Outputs']['CloudChaosMessage'] = {} 
            template['Outputs']['CloudChaosMessage']['Value'] = message
            template['Outputs']['CloudChaosSolution'] = {}
            template['Outputs']['CloudChaosSolution']['Value'] = value + " instead of " + target
            template.pop('CCSMessages')
            template.pop('CCSEvents')
            template.pop('CCSTemplateFormatVersion')
        template = walk(template)
    return template
        

def walk(node):
    if isinstance(node, dict):
        for a, b in node.items():
            if a.startswith('&&'):
                if a[2:] == target:
                    node.pop(a)
                return { swap(k): walk(v) for k, v in node.items() }
        return { swap(k): walk(v) for k, v in node.items() }
    elif isinstance(node, list):
        return [walk(elem) for elem in node]
    elif isinstance(node, str):
        node=swap(node)
        return node
    else:
        return node

def swap(key):
    defaultNeeded = False
    if key.startswith('&&'):
        defaultNeeded = True
        key = key[2:]
    if key == target:
        return value
    elif defaultNeeded:
        return fields[key]['Default']
    else:
        return key

def send_email():
    response = client.publish(
        TopicArn='arn:aws:sns:us-east-1:427334285330:CloudChaosMacro-Topic-11A96R9N6ZEX2',
        Message=message,
        Subject=subject
    )

def lambda_handler(event, context):
    parsed_template = load_monkeys(event['fragment'])
    print('parsed template')
    print(parsed_template)
    send_email()
    macro_response = {
        "requestId": event["requestId"],
        "status": "success",
		"fragment": parsed_template
    }
    return macro_response

def main(cf_template):
    f = open(cf_template[0], "r")
    r = f.read()
    fake_cf_event = {
        "requestId": "123456789",
		"fragment": json.loads(r)
    }
    lambda_handler(fake_cf_event,False)

if __name__ == '__main__':
    print('running local')
    main(sys.argv[1:])
else:
    print('running in Lambda')