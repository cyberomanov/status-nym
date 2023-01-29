import json

import requests
from loguru import logger

from datatypes.config import Nym
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
        balance=explorer.get_owner_balance(),
        owner_delegation=explorer.get_owner_delegation()
    )


def get_nym_message(report: NymReport, price: float) -> Message:
    hour_uptime_for_alarm = 80
    denom = 1_000_000

    head = f"nym ⠀|⠀ {report.description.name}"
    message = Message(status=Status.LOG, head=head, body='')
    logger.success(report.description.name)

    # report.uptime.last_hour = 62
    if report.uptime.last_hour < hour_uptime_for_alarm:
        message.status = Status.ALARM
        text = f"_hour/day > {int(report.uptime.last_hour)}%/{int(report.uptime.last_day)}%."
        logger.warning(text)
        message.body += text + '\n'
    else:
        text = f"hour/day > {int(report.uptime.last_hour)}%/{int(report.uptime.last_day)}%."
        logger.info(text)

    # report.info.outdated = True
    if report.info.outdated:
        message.status = Status.ALARM
        text = f"_version > {report.info.mixnode.version}."
        logger.warning(text)
        message.body += text + '\n'
        text = f"_outdated > true."
        logger.warning(text)
        message.body += text + '\n'
    else:
        text = f"version > {report.info.mixnode.version}."
        logger.info(text)
        text = f"outdated > false."
        logger.info(text)

    # report.info.mixnode.status = 'inactive'
    if report.info.mixnode.status != 'active':
        message.status = Status.ALARM
        text = f"_status > inactive."
        logger.warning(text)
        message.body += text + '\n'
    else:
        text = f"status > active."
        logger.info(text)

    delegations = report.info.mixnode.total_delegation.amount
    bond = report.info.mixnode.pledge_amount.amount
    total_stake = round((delegations + bond) / denom, 2)
    if price > 0:
        total_stake_usd = round(total_stake * price, 2)
        text = f"stake > {total_stake:.2f}, ${total_stake_usd:.2f}."
    else:
        text = f"stake > {total_stake:.2f}."
    message.body += text + '\n'
    logger.info(text)

    self_delegation = 0
    for delegation in report.owner_delegation:
        if delegation.mixId == report.info.mixnode.mix_id:
            self_delegation = round(delegation.amount.amount / denom, 2)
    self_stake = round(bond / denom + self_delegation, 2)
    if price > 0:
        total_self_stake_usd = round(self_stake * price, 2)
        text = f"self-stake > {self_stake:.2f}, ${total_self_stake_usd:.2f}."
    else:
        text = f"self-stake > {self_stake:.2f}."
    message.body += text + '\n'
    logger.info(text)

    rewards_per_hour = report.rewards.operator
    rewards_per_month = round(rewards_per_hour * 720 / denom, 2)
    if price > 0:
        rewards_per_month_usd = round(rewards_per_month * price, 2)
        text = f"income > {rewards_per_month:.2f}, ${rewards_per_month_usd:.2f}."
    else:
        text = f"income > {rewards_per_month:.2f}."
    message.body += text + '\n'
    logger.info(text)

    claimable = round(report.balance.claimable.amount / denom, 2)
    if price > 0:
        claimable_usd = round(claimable * price, 2)
        text = f"unpaid > {claimable:.2f}, ${claimable_usd:.2f}."
    else:
        text = f"unpaid > {claimable:.2f}."
    message.body += text + '\n'
    logger.info(text)

    spendable = round(report.balance.spendable.amount / denom, 2)
    if price > 0:
        spendable_usd = round(spendable * price, 2)
        text = f"balance > {spendable:.2f}, ${spendable_usd:.2f}."
    else:
        text = f"balance > {spendable:.2f}."
    message.body += text + '\n'
    logger.info(text)

    message.body = _format_body(body=message.body)
    return message


def _get_max_match_index(text: str | list, pattern: str) -> int:
    if isinstance(text, str):
        text = text.split('\n')

    max_index = 0
    for string in text:
        if string.rfind(pattern) > max_index:
            max_index = string.find(pattern)
    return max_index


def _text_align_by_arrow(text: str | list, max_arrow_index: int) -> str:
    if isinstance(text, str):
        text = text.split('\n')

    new_body = ''
    for string in text:
        if len(string):
            while string.rfind('>') != max_arrow_index:
                string = string.replace('>', '>>', 1)
            new_body += string + '\n'
    return new_body


def _text_align_by_usd(text: str | list, max_arrow_index: int, max_usd_index: int) -> str:
    if isinstance(text, str):
        text = text.split('\n')

    new_body = ''
    for string in text:
        if '$' in string:
            while string.rfind('$') != max_usd_index:
                string = string[:max_arrow_index + 1] + ' ' + string[max_arrow_index + 1:]
            new_body += string.replace(', ', ' | ') + '\n'
        else:
            new_body += string + '\n'
    return new_body


def _format_body(body: str) -> str:
    max_arrow_index = _get_max_match_index(text=body, pattern='>')
    new_body = _text_align_by_arrow(text=body, max_arrow_index=max_arrow_index)

    max_usd_index = _get_max_match_index(text=new_body, pattern='$')
    new_body = _text_align_by_usd(text=new_body, max_arrow_index=max_arrow_index, max_usd_index=max_usd_index)

    if not new_body.startswith('stake'):
        new_body = new_body.replace('stake', '\nstake', 1)

    return new_body
