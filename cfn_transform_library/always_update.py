from __future__ import absolute_import, print_function

import datetime

from cfn_transform import CloudFormationTemplateTransform

class AlwaysUpdate(CloudFormationTemplateTransform):
    def process_resource(self, resource_name, resource):
        if resource.get('Metadata', {}).get('AlwaysUpdate', False):
            if 'Properties' not in resource:
                resource['Properties'] = {}
            resource['Properties']['AlwaysUpdateNonce'] = datetime.datetime.utcnow().isoformat() + 'Z'

if __name__ == '__main__':
    AlwaysUpdate.main()