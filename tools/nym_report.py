from datatypes.config import Settings
from datatypes.report import NymReport, Description, Uptime
from sdk.explorer import Explorer
from tools.harbor import get_harbor_response


def get_nym_report(identity: str, setting: Settings):
    explorer = Explorer(identity=identity)
    mixnode = explorer.get_mixnode_response(identity=identity)

    return NymReport(
        description=Description(
            host=mixnode.mix_node.host,
            location=mixnode.location.three_letter_iso_country_code
        ),
        uptime=Uptime(
            last_day=mixnode.node_performance.last_24h,
            last_hour=mixnode.node_performance.last_hour,
        ),
        mixnode=mixnode,
        harbor=get_harbor_response(
            mixnode_id=mixnode.mix_id,
            mobile_proxy=setting.mobile_proxy,
            change_ip_url=setting.change_ip_url
        ),
        # balance=explorer.get_balance(address=mixnode.owner),
        owner_delegation=explorer.get_owner_delegation(mixnode_id=mixnode.mix_id)
    )
