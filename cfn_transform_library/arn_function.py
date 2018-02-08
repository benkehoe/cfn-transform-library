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
        