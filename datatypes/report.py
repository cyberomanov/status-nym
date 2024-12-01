from pydantic import BaseModel

from datatypes.delegation import DelegationResponse
from datatypes.explorer import NodeModel
from datatypes.harbor import HarborResponse


class Description(BaseModel):
    host: str


class Uptime(BaseModel):
    last_day: float
    last_hour: float


class Rewards(BaseModel):
    operator: float


class Price(BaseModel):
    usd: float


class NymPrice(BaseModel):
    nym: Price


class DenomValue(BaseModel):
    amount: float
    denom: str


class Balance(BaseModel):
    spendable: DenomValue
    delegated: DenomValue
    claimable: DenomValue
    selfBonded: DenomValue


class NymReport(BaseModel):
    description: Description
    uptime: Uptime
    mixnode: NodeModel
    harbor: HarborResponse
    # rewards: Rewards
    # balance: Balance
    owner_delegation: list[DelegationResponse]
