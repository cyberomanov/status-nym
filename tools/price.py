import json

import requests
from loguru import logger

from datatypes.report import NymPrice


def get_price(token: str = 'nym') -> float:
    response = requests.get(url=f"https://api.coingecko.com/api/v3/simple/price?ids={token}&vs_currencies=usd")
    try:
        response_parsed = NymPrice.parse_obj(json.loads(response.content))
        return response_parsed.nym.usd
    except Exception as e:
        logger.exception(e)
        return 0
