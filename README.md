# CloudChaos

CloudChaos is a CloudFormation Macro that formats special templates -- CloudChaos templates -- that include rules for breaking templates randomly each time the stack is updated, based on predefined events, and sending a message telling you whats broken this time. Suitable for testing, training, or challenging yourself in JSON or YAML.

## Install

Before using a CloudChaos template, you need to launch the CloudChaosMacro.yaml stack in the region you want to work in. You'll also need to provide an email address to get email notifications on what's wrong with the stack.

## Run Template

When you run a CloudChaos template for the first time, you'll need to provide the ARN of the SNS topic created by the macro; you can find this in the 'outputs' tab for the macro. You'll also need to provide any other fields required by that particular stack.

To get a stack, you can delete the stack and make a new one, and you'll get a new bug to fix. You can also update the stack and reupload the template -- but don't be tempted to cheat by watching what updates!

## Write

Start by replacing the values you want to (potentially) change with a keyname that begins with the && ('&&Value'). Keynames may not match the names of resources in the template. Adding && in front of a resource name will mark it for potential deletion. 

In the example below, an EC2 instance can be deleted; but it may be also be launched in the wrong subnet. IMPORTANT: in YAML, the names of resources must be surrounded by quotes.

                  '&&DeleteInstanceEvent':
                    Type: AWS::EC2::Instance
                    Properties:
                      SubnetId: !Ref '&&InstanceSubnetEvent'
                      
  
### Events

For the chaos to happen, each key needs a matching entry in CCEvents. The macro uses CCEvents as the master list of all the things that can go wrong, selecting a new event at random each time.

      DeleteInstanceEvent:
        Default: "Instance"
        Type: delete
        Events:
          - NoSSH
          - ServerFailure
      InstanceSubnetEvent:
        Default: PublicSubnet
        Type: alter
        Values:
          - 1.1.1.1/32
        Events:
          - NoSSH
          - LambdaFailure
          - ServerFailure

 Delete events must have the same name as the resource being deleted. Adding && may lead to templates that will fail on launch. 

        "EmptyBucket":{
            "Type": "delete",
            "Events": ["MissingBucket"]
        },

### CCMessages




All templates should be tested thoroughly before being distributed.

## Template

A CloudChaos template is a regular CloudFormation template with extra fields. The macro need the following header to work right: 

  "AWSTemplateFormatVersion": "2010-09-09",
    "CCSTemplateFormatVersion": "2020-06-09",
    "Parameters" : {
        "MacroNameParam" : {
          "Type" : "String",
          "Default": "CloudChaosMacro",
          "Description" : "Name of the CloudChaosMacro."
        },
        "SNSTopic":{
          "Type" : "String",
          "Default": "CloudChaosMacro",
          "Description" : "Name of the CloudChaosSNSTopic."
        }
    }
    
CloudChaos will look for two other fields: CCFields and CCEvents. CCFields are the fields you want to be able to break.

## Test

