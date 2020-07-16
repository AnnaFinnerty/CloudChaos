# CloudChaos

CloudChaos is a CloudFormation Macro that formats special templates -- CloudChaos templates -- that include rules for breaking templates at randomly each time the stack is updated, based on predefined events. User messages provide feedback on the error occuring. Suitable for testing, training, or challenging yourself.

## Install

First create a Lambda function and upload function.zip to it. Copy the arn of that Lambda, you'll need it in a second.

Next, create a CloudFormation stack using macro.yaml as a template. You will need to provide two variables: the arn of the Lambda you just created, and the email address you want to recieve user messages on.

## Run

After the Macro is installed, CloudChaos templates can be launched like normal CloudFormation templates. If CloudChaos templates are launched when the macro is not installed/in another region, the template launch will fail.

## Write

To create you own CloudChaos templates to run with the macro, start by identifying parts of a template you want to be able to randomly effect. Remove those values, and replace it with a label that begins with the &&:
                    {
                        "Key": "keyname",
                        "Value": "&&chaos"
                    }

### CCEvents

Now, create a event in CCEvents, with the same name as the label. 

      "bucket1field":{
            "Type": "random",
            "Default": "emptyBucket tag",
            "Values":["red","blue","green"],
            "Weights":["1","1","1"],
            "Events": ["MissingBucket","WriteFailed"]
        },

Adding && in front of a resource name will mark it for potential deletion. Delete events must have the same name as the resource being deleted.

        "EmptyBucket":{
            "Type": "delete",
            "Events": ["MissingBucket"]
        },

Adding && in front of other field may break the macro, and lead to templates that will fail on launch.

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

