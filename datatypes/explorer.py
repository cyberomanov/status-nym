from pydantic import BaseModel


class DenomValue(BaseModel):
    amount: float
    denom: str


class Mixnode(BaseModel):
    host: str
    http_api_port: str
    version: str
    mix_id: int
    owner: str
    uptime: float
    status: str
    pledge_amount: DenomValue
    total_delegation: DenomValue
    operating_cost: DenomValue


class Info(BaseModel):
    mixnode: Mixnode
    outdated: bool


class Uptime(BaseModel):
    last_day: float
    last_hour: float


class Rewards(BaseModel):
    operator: float


class Price(BaseModel):
    usd: float


class NymPrice(BaseModel):
    nym: Price


class Balance(BaseModel):
    spendable: DenomValue
    claimable: DenomValue


class OwnerDelegation(BaseModel):
    amount: DenomValue
    mixId: int
    block: int
    identityKey: str
    moniker: str


class Description(BaseModel):
    name: str
    description: str
    link: str
    location: str


class NymReport(BaseModel):
    description: Description
    uptime: Uptime
    info: Info
    rewards: Rewards
    balance: Balance
    owner_delegation: list[OwnerDelegation]
