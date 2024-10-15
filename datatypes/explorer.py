from typing import Optional

from pydantic import BaseModel


class Location(BaseModel):
    two_letter_iso_country_code: str
    three_letter_iso_country_code: str
    country_name: str
    latitude: float
    longitude: float


class PledgeAmount(BaseModel):
    denom: str
    amount: str


class TotalDelegation(BaseModel):
    denom: str
    amount: str


class MixNode(BaseModel):
    host: str
    mix_port: int
    verloc_port: int
    http_api_port: int
    sphinx_key: str
    identity_key: str
    version: str


class NodePerformance(BaseModel):
    most_recent: str
    last_hour: str
    last_24h: str


class OperatingCost(BaseModel):
    denom: str
    amount: str


class MixNodeModel(BaseModel):
    mix_id: int
    location: Optional[Location]
    status: str
    pledge_amount: PledgeAmount
    total_delegation: TotalDelegation
    owner: str
    layer: int
    mix_node: MixNode
    stake_saturation: float
    uncapped_saturation: float
    avg_uptime: int
    node_performance: NodePerformance
    estimated_operator_apy: float
    estimated_delegators_apy: float
    operating_cost: OperatingCost
    profit_margin_percent: str
    family_id: Optional[str]
    blacklisted: bool
