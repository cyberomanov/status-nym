from loguru import logger

from sdk.telegram import Telegram
from utils.create_logger import add_logger
from utils.get_config import get_config
from utils.tools import get_price, get_nym_report, get_nym_message


def nym():
    try:
        add_logger()
        config = get_config()
        settings, identities = config.settings, config.identity

        telegram = Telegram(bot_api_token=settings.bot_api_key,
                            log_chat_id=settings.log_chat_id,
                            alarm_chat_id=settings.alarm_chat_id)

        price = get_price()

        for identity in identities:
            report = get_nym_report(identity=identity)
            message = get_nym_message(report=report, price=price)

            if message.status:
                telegram_response = telegram.send_log(head=message.head, body=message.body)
            else:
                telegram_response = telegram.send_alarm(head=message.head, body=message.body)

            if not telegram_response.ok:
                logger.error(
                    f"telegram response is not ok. "
                    f"code: {telegram_response.error_code}, "
                    f"description: {telegram_response.description}."
                )
            else:
                logger.warning(f"telegram message successfully sent.")

    except Exception as e:
        logger.exception(e)
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    nym()
