import json

import requests

from datatypes.explorer import Info, Uptime, Rewards, Balance, Description, OwnerDelegation


class Explorer:
    def __init__(self, identity: str, explorer: str = "https://mixnet.api.explorers.guru/api"):
        self.identity = identity
        self.explorer = explorer

        self.session = self._create_session()
        self.mixnode_info = self.get_mixnode_info()

        self.mixnode_id = self.mixnode_info.mixnode.mix_id
        self.owner = self.mixnode_info.mixnode.owner

    @staticmethod
    def _create_session():
        return requests.session()

    def _get_mixnode_info(self, specific: str = None) -> Info | Uptime | Rewards:
        if specific:
            url = f"{self.explorer}/mixnodes/{self.mixnode_id}/{specific}"
        else:
            url = f"{self.explorer}/mixnodes/{self.identity}"
        return json.loads(self.session.get(url).content)

    def get_mixnode_info(self) -> Info:
        return Info.parse_obj(self._get_mixnode_info())

    def get_mixnode_uptime(self) -> Uptime:
        return Uptime.parse_obj(self._get_mixnode_info(specific='uptime'))

    def get_estimated_rewards(self) -> Rewards:
        response = self._get_mixnode_info(specific='estimated_reward')
        try:
            return Rewards.parse_obj(response)
        except:
            return Rewards(operator=0)

    def get_owner_balance(self) -> Balance:
        response = self.session.get(f"{self.explorer}/accounts/{self.owner}/balance")
        return Balance.parse_obj(json.loads(response.content))

    def get_owner_delegation(self) -> list[OwnerDelegation]:
        owner_delegations = []
        response = self.session.get(f"{self.explorer}/accounts/{self.owner}/delegations")
        delegation_list = json.loads(response.content)
        for delegation in delegation_list:
            owner_delegations.append(OwnerDelegation.parse_obj(delegation))
        return owner_delegations

    def get_mixnode_description(self) -> Description:
        response = self.session.get(f"{self.explorer}/mixnodes/description?"
                                    f"ip={self.mixnode_info.mixnode.host}&"
                                    f"port={self.mixnode_info.mixnode.http_api_port}")
        return Description.parse_obj(json.loads(response.content))
