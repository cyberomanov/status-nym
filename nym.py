from loguru import logger

from datatypes.config import Settings
from sdk.telegram import Telegram
from tools.add_logger import add_logger
from tools.get_config import get_config
from tools.nym_message import get_nym_message
from tools.nym_report import get_nym_report
from tools.price import get_price


def nym(settings: Settings, identity: str, price: float, telegram: Telegram):
    try:
        report = get_nym_report(identity=identity, settings=settings)
    except Exception as e:
        telegram_response = telegram.send_log(head="nym", dashboard='', body="bad response.")
        if not telegram_response.ok:
            logger.error(
                f"telegram response is not ok. "
                f"code: {telegram_response.error_code}, "
                f"description: {telegram_response.description}."
            )
        else:
            logger.warning(f"telegram message successfully sent.")
        logger.error(f"bad response: {e}")
        return

    message = get_nym_message(report=report, price=price)

    if message.status.value == 0:
        logger.success('no warnings found.')
        telegram_response = telegram.send_log(
            head=message.head, dashboard=message.dashboard, body=message.body
        )
    else:
        logger.warning('something is not ok.')
        telegram_response = telegram.send_log(
            head=message.head, dashboard=message.dashboard, body=message.body
        )
        telegram_response = telegram.send_alarm(
            head=message.head, dashboard=message.dashboard, body=message.body
        )

    if not telegram_response.ok:
        logger.error(
            f"telegram response is not ok. "
            f"code: {telegram_response.error_code}, "
            f"description: {telegram_response.description}."
        )
    else:
        logger.warning(f"telegram message successfully sent.")


if __name__ == '__main__':
    add_logger(version='v3.0')
    try:
        config = get_config()
        settings, identities = config.settings, config.identity
        telegram = Telegram(
            bot_api_token=settings.bot_api_key,
            log_chat_id=settings.log_chat_id,
            alarm_chat_id=settings.alarm_chat_id
        )
        price = get_price()

        for identity in identities:
            nym(
                settings=settings,
                identity=identity,
                price=price,
                telegram=telegram
            )
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        logger.exception(e)
