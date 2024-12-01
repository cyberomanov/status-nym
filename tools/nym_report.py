from datatypes.config import Settings
from datatypes.report import NymReport, Description, Uptime
from sdk.explorer import Explorer
from tools.harbor import get_harbor_response


def get_nym_report(identity: str, settings: Settings):
    explorer = Explorer(identity=identity)
    mixnode = explorer.get_mixnode_response(identity=identity)
    harbor = get_harbor_response(mixnode_id=mixnode.node_id, mobile_proxy=settings.mobile_proxy)
    return NymReport(
        description=Description(
            host=harbor.self_described.self_described.host_information.hostname
            if harbor.self_described.self_described.host_information.hostname
            else harbor.self_described.self_described.host_information.ip_address[0],
            location=harbor.self_described.self_described.auxiliary_details.location
            if harbor.self_described.self_described.auxiliary_details.location
            else ""
        ),
        uptime=Uptime(
            last_day=harbor.full_details.node_performance.last_24h,
            last_hour=harbor.full_details.node_performance.last_hour,
        ),
        mixnode=mixnode,
        harbor=harbor,
        owner_delegation=explorer.get_owner_delegation(mixnode_id=str(harbor.mix_id))
    )
