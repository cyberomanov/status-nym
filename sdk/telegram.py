import requests

from datatypes.telegram import Response


class Telegram:
    def __init__(self,
                 bot_api_token: str,
                 log_chat_id: str,
                 alarm_chat_id: str):
        self.bot_api_token = bot_api_token
        self.log_chat_id = log_chat_id
        self.alarm_chat_id = alarm_chat_id

    def _send_message(self, text: str, chat_id: str, parse_mode: str = "HTML") -> Response:
        response = requests.post(
            f"https://api.telegram.org/bot{self.bot_api_token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode,
            }
        ).json()
        return Response.parse_obj(response)

    def send_log(self, head: str, body: str) -> Response:
        text = f"<b>{head}</b>\n\n" \
               f"<code>{body}</code>"
        return self._send_message(text=text, chat_id=self.log_chat_id)

    def send_alarm(self, head: str, body: str) -> Response:
        text = f"<b>{head}</b>\n\n" \
               f"<code>{body}</code>"
        return self._send_message(text=text, chat_id=self.alarm_chat_id)
