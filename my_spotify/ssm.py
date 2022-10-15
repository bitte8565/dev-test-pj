# -*- coding: utf-8 -*-

def get_parameters(self, param_key):
    response = self.ssm.get_parameters(
        Names=[
            param_key,
        ],
        WithDecryption=True
    )
    return response['Parameters'][0]['Value']
