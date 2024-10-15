from loguru import logger

from datatypes.message import Message, Status
from datatypes.report import NymReport


def get_nym_message(report: NymReport, price: float, ignore_inactive: bool) -> Message:
    hour_uptime_for_alarm = 80
    denom = 1_000_000

    head = f"nym ⠀|⠀ {report.harbor.description.moniker}"
    message = Message(status=Status.LOG, head=head, body='')
    logger.success(report.harbor.description.moniker)

    if int(report.uptime.last_hour * 100) < hour_uptime_for_alarm:
        message.status = Status.ALARM
        text = f"_hour/day > {int(report.uptime.last_hour * 100)}%/{int(report.uptime.last_day * 100)}%."
        logger.warning(text)
        message.body += text + '\n'
    else:
        text = f"hour/day > {int(report.uptime.last_hour * 100)}%/{int(report.uptime.last_day * 100)}%."
        logger.info(text)

    text = f"version > {report.harbor.self_described.bond.mix_node.version}."
    logger.info(text)
    message.body += text + '\n'

    if report.mixnode.status != 'active':
        if not ignore_inactive:
            message.status = Status.ALARM
        text = f"_status > inactive."
        logger.warning(text)
        message.body += text + '\n'
    else:
        text = f"status > active."
        logger.info(text)

    total_stake = round(report.harbor.total_stake / denom, 2)
    if price > 0:
        total_stake_usd = round(total_stake * price, 2)
        text = f"stake > {total_stake:.2f}, ${total_stake_usd:.2f}."
    else:
        text = f"stake > {total_stake:.2f}."
    message.body += text + '\n'
    logger.info(text)

    self_delegations_amount = 0
    for delegation in report.owner_delegation:
        if delegation.owner.lower() == report.mixnode.owner.lower():
            self_delegations_amount += round(int(delegation.amount.amount) / denom, 2)

    self_bond = round(int(report.harbor.full_details.mixnode_details.bond_information.original_pledge.amount) / denom,
                      2)
    self_stake = round(self_delegations_amount + self_bond, 2)
    if price > 0:
        total_self_stake_usd = round(self_stake * price, 2)
        text = f"self-stake > {self_stake:.2f}, ${total_self_stake_usd:.2f}."
    else:
        text = f"self-stake > {self_stake:.2f}."
    message.body += text + '\n'
    logger.info(text)

    # rewards_per_hour = report.rewards.operator
    # rewards_per_month = round(rewards_per_hour * 720 / denom, 2)
    # if price > 0:
    #     rewards_per_month_usd = round(rewards_per_month * price, 2)
    #     text = f"income > {rewards_per_month:.2f}, ${rewards_per_month_usd:.2f}."
    # else:
    #     text = f"income > {rewards_per_month:.2f}."
    # message.body += text + '\n'
    # logger.info(text)
    #
    # claimable = round(report.balance.claimable.amount / denom, 2)
    # if price > 0:
    #     claimable_usd = round(claimable * price, 2)
    #     text = f"unpaid > {claimable:.2f}, ${claimable_usd:.2f}."
    # else:
    #     text = f"unpaid > {claimable:.2f}."
    # message.body += text + '\n'
    # logger.info(text)
    #
    # spendable = round(report.balance.spendable.amount / denom, 2)
    # if price > 0:
    #     spendable_usd = round(spendable * price, 2)
    #     text = f"balance > {spendable:.2f}, ${spendable_usd:.2f}."
    # else:
    #     text = f"balance > {spendable:.2f}."
    # message.body += text + '\n'
    # logger.info(text)

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
