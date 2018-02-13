# cfn-transform-library

A set of CloudFormation transforms using [cfn-transform](https://github.com/benkehoe/cfn-transform).
Install that, and use like:

```
cfn-transform cfn_transform_library.<transform_name> [-i TEMPLATE_FILE] [-o OUTPUT_FILE]
```
Note that there are other command line options, see the `cfn-transform` repo for more details.

## arn_function

This transform gives you the ability to easily define [ARNs](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)
in your templates, wihtout worrying about getting the region, account, etc. right.
To use it, first install the `aws-arn` library:

```
pip install git+git://github.com/benkehoe/aws-arn
```

Then, in your template, you can specify ARNs like so:
```
{"Fn::Arn": [<service_name>, <resource_name>]}
-OR-
{"Fn::Arn": [<service_name>, <resource_name_part>, <resource_name_part>, ...]}
```
and this will get turned into a CloudFormation `Fn::Join` that formats the appropriate ARN for the
given service. In the second form, all of the `resource_name_parts` will get concatenated, allowing
you to use references. For example, suppose you have a parameter on the template that is the name
of a DynamoDB table, and you need to construct the ARN for an IAM policy (note that if the the table was
a resource inside the template, the ARN would be available as an attribute on that resource). You
can construct the ARN as follows:

```
{"Fn::Arn": ["dynamodb", "table/", {"Ref": "TableNameParameter"}]}
``` 

## always_update

This transform is meant for use with [CloudFormation custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html),
which sometimes need to be updated every time the stack is updated,
even if the properties of the resource don't change. In this case,
use this transform and put `{"AlwaysUpdate": true}` in the
`Metadata` section of the resource. This transform will set
a property `AlwaysUpdateNonce` on the resource that will
be a string that should change every time it is called.
Currently, the string is a ISO8601 UTC timestamp with millisecond
precision, but this is not intended to be relied upon. 