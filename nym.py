from loguru import logger

from sdk.telegram import Telegram
from utils.create_logger import add_logger
from utils.get_config import get_config
from utils.tools import get_price, get_nym_report, get_nym_message


def nym():
    try:
        add_logger(version='v1.5')
        config = get_config()
        settings, identities = config.settings, config.identity
        telegram = Telegram(bot_api_token=settings.bot_api_key,
                            log_chat_id=settings.log_chat_id,
                            alarm_chat_id=settings.alarm_chat_id)
        price = get_price()

        for identity in identities:
            try:
                report = get_nym_report(identity=identity)
            except Exception as e:
                telegram_response = telegram.send_log(head="nym", body="response from 'nodes.guru' is not ok.")
                if not telegram_response.ok:
                    logger.error(
                        f"telegram response is not ok. "
                        f"code: {telegram_response.error_code}, "
                        f"description: {telegram_response.description}."
                    )
                else:
                    logger.warning(f"telegram message successfully sent.")
                logger.error(f"response from 'nodes.guru' is not ok: {e}")
                break

            message = get_nym_message(report=report, price=price, ignore_inactive=settings.ignore_inactive)

            if message.status.value == 0:
                logger.success('no warnings found.')
                telegram_response = telegram.send_log(head=message.head, body=message.body)
            else:
                logger.warning('something is not ok.')
                telegram_response = telegram.send_log(head=message.head, body=message.body)
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
