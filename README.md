# CloudChaos

CloudChaos is a CloudFormation Macro that formats special templates -- CloudChaos templates -- that include rules for breaking templates at randomly each time the stack is updated, based on predefined events. User messages provide feedback on the error occuring. Suitable for testing, training, or challenging yourself.

## Basics

A CloudChaos template is a regular CloudFormation template with extra fields. The macro need the following header to work right: 

``` "AWSTemplateFormatVersion": "2010-09-09",
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
    }```

CloudChaos will look for two other fields: CCFields and CCEvents. CCFields are the fields you want to be able to break.

## Install

To install the macro, first create a Lambda function and upload function.zip to it. Copy the arn of that Lambda, you'll need it in a second.

Next, create a CloudFormation stack using macro.yaml as a template. You will need to provide two variables: the arn of the Lambda you just created, and the email address you want to recieve user messages on.

## Run

To launch a CloudChaos template

## Run Locally

