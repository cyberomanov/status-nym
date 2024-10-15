import json

from loguru import logger

from datatypes.harbor import HarborResponse
from tools.change_ip import execute_change_ip
from tools.other_utils import get_proxied_session


def get_harbor_response(mixnode_id: int, mobile_proxy: str, change_ip_url: str):
    if change_ip_url:
        change_ip = execute_change_ip(change_ip_url=change_ip_url)
        if change_ip:
            logger.info(f"mix_id: {mixnode_id} | ip has been changed.")
        else:
            logger.error(f"mix_id: {mixnode_id} | ip has not been changed.")
            return
    url = f"https://harbourmaster.nymtech.net/v2/mixnodes/{mixnode_id}"
    response = get_proxied_session(proxy=mobile_proxy).get(url=url)
    return HarborResponse.parse_obj(json.loads(response.content))
