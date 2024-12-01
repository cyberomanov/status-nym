from pydantic import BaseModel


class Nym(BaseModel):
    moniker: str
    identity: str


class Settings(BaseModel):
    bot_api_key: str
    alarm_chat_id: str
    log_chat_id: str
    mobile_proxy: str
    change_ip_url: str


class Config(BaseModel):
    identity: list[str]
    settings: Settings
