from pydantic import BaseModel


class Nym(BaseModel):
    moniker: str
    identity: str


class Settings(BaseModel):
    ignore_inactive: bool
    bot_api_key: str
    alarm_chat_id: str
    log_chat_id: str


class Config(BaseModel):
    identity: list[str]
    settings: Settings
