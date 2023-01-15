import json

import requests
from loguru import logger

from datatypes.config import Nym, Settings
from datatypes.explorer import NymPrice, NymReport
from datatypes.message import Message, Status
from sdk.explorer import Explorer


def get_nym_instances(nym_instances: dict[str, str]) -> list[Nym]:
    instances = []
    for nym in nym_instances.items():
        instances.append(Nym(moniker=nym[0], identity=nym[1]))
    return instances


def get_price() -> float:
    response = requests.get(url="https://api.coingecko.com/api/v3/simple/price?ids=nym&vs_currencies=usd")
    try:
        response_parsed = NymPrice.parse_obj(json.loads(response.content))
        return response_parsed.nym.usd
    except Exception as e:
        logger.exception(e)
        return 0


def get_nym_report(identity: str) -> NymReport:
    explorer = Explorer(identity=identity)
    return NymReport(
        description=explorer.get_mixnode_description(),
        uptime=explorer.get_mixnode_uptime(),
        info=explorer.get_mixnode_info(),
        rewards=explorer.get_estimated_rewards(),
        balance=explorer.get_owner_balance()
    )


def get_nym_message(report: NymReport, price: float) -> Message:
    hour_uptime_for_alarm = 80
    denom = 1_000_000

    head = f"nym | {report.description.name}"
    message = Message(status=Status.LOG, head=head, body='')
    logger.success(head)

    if report.uptime.last_hour < hour_uptime_for_alarm:
        message.status = Status.ALARM
        text = f"_hour/day: {report.uptime.last_hour}%/{report.uptime.last_day}%"
        logger.warning(text)
        message.body += text + '\n'
    else:
        text = f"hour/day: {report.uptime.last_hour}%/{report.uptime.last_day}%"
        logger.info(text)

    if report.info.outdated:
        message.status = Status.ALARM
        text = f"_version: {report.info.mixnode.version}"
        logger.warning(text)
        message.body += text + '\n'
        text = f"_outdated: true"
        logger.warning(text)
        message.body += text + '\n'
    else:
        text = f"version: {report.info.mixnode.version}"
        logger.info(text)
        text = f"outdated: false"
        logger.info(text)

    if report.info.mixnode.status != 'active':
        message.status = Status.ALARM
        text = f"_status: inactive"
        logger.warning(text)
        message.body += text + '\n'
    else:
        text = f"status: active"
        logger.info(text)

    delegations = report.info.mixnode.total_delegation.amount
    self_stake = report.info.mixnode.pledge_amount.amount
    total_stake = round((delegations + self_stake) / denom, 2)
    total_stake_usd = round(total_stake * price, 2)
    text = f"stake: {total_stake}, ${total_stake_usd}"
    message.body += text + '\n'
    logger.info(text)

    rewards_per_hour = report.rewards.operator
    rewards_per_month = round(rewards_per_hour * 720 / denom, 2)
    rewards_per_month_usd = round(rewards_per_month * price, 2)
    text = f"salary: {rewards_per_month}, ${rewards_per_month_usd}"
    message.body += text + '\n'
    logger.info(text)

    claimable = round(report.balance.claimable.amount / denom, 2)
    claimable_usd = round(claimable * price, 2)
    text = f"unpaid: {claimable}, ${claimable_usd}"
    message.body += text + '\n'
    logger.info(text)

    spendable = round(report.balance.spendable.amount / denom, 2)
    spendable_usd = round(spendable * price, 2)
    text = f"balance: {spendable}, ${spendable_usd}"
    message.body += text + '\n'
    logger.info(text)

    return message
