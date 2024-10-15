import json

import requests

from datatypes.harbor import HarborResponse


def get_harbor_response(mixnode_id: int):
    url = f"https://harbourmaster.nymtech.net/v2/mixnodes/{mixnode_id}"
    response = requests.get(url=url)
    return HarborResponse.parse_obj(json.loads(response.content))
