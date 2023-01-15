from pydantic import BaseModel


class Nym(BaseModel):
    moniker: str
    identity: str


class Settings(BaseModel):
    bot_api_key: str
    alarm_chat_id: str
    log_chat_id: str
   #  hour_uptime_for_alarm: int


class Config(BaseModel):
    identity: list[str]
    settings: Settings
