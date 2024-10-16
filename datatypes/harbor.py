from typing import List, Optional, Dict
from pydantic import BaseModel


class Location(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]


class PledgeAmount(BaseModel):
    denom: str
    amount: str


class MixNode(BaseModel):
    host: str
    http_api_port: int
    identity_key: str
    mix_port: int
    sphinx_key: str
    verloc_port: int
    version: str


class BondInformation(BaseModel):
    bonding_height: int
    is_unbonding: bool
    layer: int
    mix_id: int
    mix_node: MixNode
    original_pledge: PledgeAmount
    owner: str
    proxy: Optional[str]


class IntervalOperatingCost(BaseModel):
    interval_operating_cost: PledgeAmount
    profit_margin_percent: str


class RewardingDetails(BaseModel):
    cost_params: IntervalOperatingCost
    delegates: str
    last_rewarded_epoch: int
    operator: str
    total_unit_reward: str
    unique_delegations: int
    unit_delegation: str


class NodePerformance(BaseModel):
    last_24h: str
    last_hour: str
    most_recent: str


class MixnodeDetails(BaseModel):
    bond_information: BondInformation
    pending_changes: Optional[Dict[str, Optional[str]]]
    rewarding_details: RewardingDetails


class FullDetails(BaseModel):
    blacklisted: bool
    estimated_delegators_apy: str
    estimated_operator_apy: str
    family: Optional[str]
    ip_addresses: List[str]
    mixnode_details: MixnodeDetails
    node_performance: NodePerformance
    performance: str
    stake_saturation: str
    uncapped_stake_saturation: str


class Authenticator(BaseModel):
    address: str


class AuxiliaryDetails(BaseModel):
    accepted_operator_terms_and_conditions: bool
    location: Optional[str]


class BuildInformation(BaseModel):
    binary_name: str
    build_timestamp: str
    build_version: str
    cargo_profile: str
    cargo_triple: str
    commit_branch: str
    commit_sha: str
    commit_timestamp: str
    rustc_channel: str
    rustc_version: str


class HostInformation(BaseModel):
    hostname: Optional[str]
    ip_address: List[str]
    keys: Dict[str, str]


class IpPacketRouter(BaseModel):
    address: str


class MixnetWebsockets(BaseModel):
    ws_port: int
    wss_port: Optional[int]


class NetworkRequester(BaseModel):
    address: str
    uses_exit_policy: bool


class Role(BaseModel):
    Mixnode: Dict[str, int]


class SelfDescribedDetails(BaseModel):
    authenticator: Optional[Authenticator]
    auxiliary_details: AuxiliaryDetails
    build_information: BuildInformation
    host_information: HostInformation
    ip_packet_router: IpPacketRouter
    last_polled: str
    mixnet_websockets: MixnetWebsockets
    network_requester: NetworkRequester
    role: Role


class SelfDescribedModel(BaseModel):
    bond: BondInformation
    self_described: Optional[SelfDescribedDetails]


class Description(BaseModel):
    moniker: str
    website: str
    security_contact: Optional[str]
    details: Optional[str]


class HarborResponse(BaseModel):
    mix_id: int
    bonded: bool
    blacklisted: bool
    is_dp_delegatee: bool
    total_stake: int
    full_details: FullDetails
    self_described: Optional[SelfDescribedModel]
    description: Description
    last_updated_utc: str
