"""Transform Fn::Arn into standard CloudFormation.

Requires the aws-arn library.

Supports syntax like:

{"Fn::Arn": [<service_name>, <resource_name>]}
-OR-
{"Fn::Arn": [<service_name>, <resource_name_part>, <resource_name_part>, ...]}

Copyright 2018 iRobot Corporation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import absolute_import, print_function

import aws_arn

from cfn_transform import CloudFormationTemplateTransform

class ArnFunction(CloudFormationTemplateTransform):
    def _replace(self, d, path=[]):
        for key in d:
            if isinstance(d[key], dict):
                if 'Fn::Arn' in d[key]:
                    value = d[key]['Fn::Arn']
                    if not isinstance(value, list):
                        raise TypeError("Input to Fn::Arn must be a list (at {})".format('/'.join(path)))
                    service = value[0]
                    resource = value[1:]
                    d[key] = aws_arn.cloudformation(service, resource)
                else:
                    self._replace(d[key], path=path+[key])
    
    def _apply(self):
        self._replace(self.template)
        