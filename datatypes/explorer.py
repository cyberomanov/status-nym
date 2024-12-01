from typing import Optional, List

from pydantic import BaseModel

from datatypes.harbor import Location


class HostInformation(BaseModel):
    ip_address: List[str]
    hostname: Optional[str]
    keys: dict


class DeclaredRole(BaseModel):
    mixnode: bool
    entry: bool
    exit_nr: bool
    exit_ipr: bool


class AuxiliaryDetails(BaseModel):
    location: Optional[str]
    announce_ports: dict
    accepted_operator_terms_and_conditions: bool


class BuildInformation(BaseModel):
    binary_name: str
    build_timestamp: str
    build_version: str
    commit_sha: str
    commit_timestamp: str
    commit_branch: str
    rustc_version: str
    rustc_channel: str
    cargo_profile: str
    cargo_triple: str


class Description(BaseModel):
    last_polled: str
    host_information: HostInformation
    declared_role: DeclaredRole
    auxiliary_details: AuxiliaryDetails
    build_information: BuildInformation
    network_requester: Optional[dict]
    ip_packet_router: Optional[dict]
    authenticator: Optional[dict]
    wireguard: Optional[dict]
    mixnet_websockets: Optional[dict]


class OriginalPledge(BaseModel):
    denom: str
    amount: str


class Node(BaseModel):
    host: Optional[str]
    custom_http_port: Optional[int]
    identity_key: str


class BondInformation(BaseModel):
    node_id: int
    owner: str
    original_pledge: OriginalPledge
    bonding_height: int
    is_unbonding: bool
    node: Node


class CostParams(BaseModel):
    profit_margin_percent: str
    interval_operating_cost: dict


class RewardingDetails(BaseModel):
    cost_params: CostParams
    operator: str
    delegates: str
    total_unit_reward: str
    unit_delegation: str
    last_rewarded_epoch: int
    unique_delegations: int


class NodeModel(BaseModel):
    node_id: int
    contract_node_type: Optional[str]
    description: Optional[Description]
    bond_information: BondInformation
    rewarding_details: RewardingDetails
    location: Optional[Location]
