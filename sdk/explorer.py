import json

import requests

from datatypes.delegation import DelegationResponse
from datatypes.explorer import NodeModel
from datatypes.report import Balance


class Explorer:
    def __init__(self, identity: str, explorer: str = "https://explorer.nymtech.net/api/v1/mix-node"):
        self.identity = identity
        self.explorer = explorer

        self.session = self._create_session()

    @staticmethod
    def _create_session():
        return requests.session()

    def _get_mixnodes_response(self):
        response = self.session.get(f"https://explorer.nymtech.net/api/v1/tmp/unstable/nym-nodes")
        try:
            return [NodeModel(**item) for item in json.loads(response.content)]
        except Exception as e:
            pass

    def get_mixnode_response(self, identity: str):
        mixnodes = self._get_mixnodes_response()
        for node in mixnodes:
            if node.bond_information.node.identity_key.lower() == identity.lower():
                return node

    def get_balance(self, address: str) -> Balance:
        response = self.session.get(f"{self.explorer}/accounts/{address}/balance")
        return Balance.parse_obj(json.loads(response.content))

    def get_owner_delegation(self, mixnode_id: str) -> list[DelegationResponse]:
        owner_delegations = []
        response = self.session.get(f"{self.explorer}/{mixnode_id}/delegations")
        delegation_list = json.loads(response.content)
        for delegation in delegation_list:
            owner_delegations.append(DelegationResponse.parse_obj(delegation))
        return owner_delegations
