import requests


def get_proxied_session(proxy: str):
    session = requests.Session()
    if proxy:
        session.proxies = {
            'http': proxy,
            'https': proxy
        }
    session.request = lambda *args, **kwargs: requests.Session.request(session, *args, timeout=60, **kwargs)
    return session
