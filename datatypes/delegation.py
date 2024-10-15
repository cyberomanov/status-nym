from typing import Optional

from pydantic import BaseModel


class Amount(BaseModel):
    denom: str
    amount: str


class DelegationResponse(BaseModel):
    owner: Optional[str]
    mix_id: Optional[int]
    cumulative_reward_ratio: Optional[str]
    amount: Optional[Amount]
    height: Optional[int]
    proxy: Optional[str]
