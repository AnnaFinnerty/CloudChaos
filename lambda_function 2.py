import sys
import json
import random

def load_monkeys(template):
    print("loading monkeys")
    # make sure this is a ccs template
    if template['CCSTemplateFormatVersion']:
        print(template['CCSTemplateFormatVersion'])
        if template['CCFields']:
            global fields, target, value
            ##load fields
            fields = template['CCFields']
            keys = list(fields.keys())
            ##choose random event from event pool
            r = random.randrange(len(keys))
            target = keys[r]
            event = fields[target]
            print('event: ')
            print(event)
            # print('target: ' + str(target))
            ##choose random value from event pool
            r = random.randrange(len(event['Values']))
            value = event['Values'][random.randrange(len(event['Values']))]
            print('value: ' + str(value))
            scenario = event['Events'][random.randrange(len(event['Events']))]
            print('scenario: ' + str(scenario))
            messages = template['CCEvents'][scenario]
            print('messages')
            print(messages)
            message = messages[random.randrange(len(messages))]
            print('message ' + message)
            ##remove flags and events
            if 'Outputs' not in template:
                 template['Outputs'] = {}
            template['Outputs']['CloudChaosScenario'] = {} 
            template['Outputs']['CloudChaosScenario']['Value'] = scenario
            template['Outputs']['CloudChaosMessage'] = {} 
            template['Outputs']['CloudChaosMessage']['Value'] = message
            template['Outputs']['CloudChaosSolution'] = {}
            template['Outputs']['CloudChaosSolution']['Value'] = value + " instead of " + target
            template.pop('CCFields')
            template.pop('CCEvents')
            template.pop('CCSTemplateFormatVersion')
        template = walk(template)
    return template
        

def walk(node):
    if isinstance(node, dict):
        return { k: walk(v) for k, v in node.items() }
    elif isinstance(node, list):
        return [walk(elem) for elem in node]
    elif isinstance(node, str):
        print('on string ' + node)
        node=swap(node)
        return node
    else:
        return node

def swap(key):
    print('original: ' + key)
    if key.startswith('&&'):
        print('swapping: ' + key)
        key = key[2:]
        print('swapped: ' + key)
    if key == target:
        return value
    else:
        print('returning: ' + key)
        return key

def lambda_handler(event, context):
    print(event)
    parsed_template = load_monkeys(event['fragment'])
    print('parsed template')
    print(parsed_template)
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
    # print(fake_cf_event)
    lambda_handler(fake_cf_event,False)

if __name__ == '__main__':
    print('running local')
    main(sys.argv[1:])
else:
    print('running in Lambda')