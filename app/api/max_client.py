import requests


class MaxClient:

    def __init__(
        self,
        token: str,
        base_url: str,
        verify_ssl: bool = True
    ):
        self.base_url = base_url
        self.verify_ssl = verify_ssl

        self.headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

    def get_updates(self, marker=None):

        params = {
            "timeout": 30
        }

        if marker is not None:
            params["marker"] = marker

        response = requests.get(
            self.base_url + "/updates",
            headers=self.headers,
            params=params,
            verify=self.verify_ssl
        )

        response.raise_for_status()

        return response.json()

    def send_message(
        self,
        chat_id: int,
        text: str,
        attachments=None
    ):

        body = {
            "text": text
        }

        if attachments is not None:
            body["attachments"] = attachments

        response = requests.post(
            self.base_url + "/messages",
            headers=self.headers,
            params={"chat_id": chat_id},
            json=body,
            verify=self.verify_ssl
        )

        response.raise_for_status()

        return response.json()

    def edit_message(
        self,
        message_id: str,
        text: str,
        attachments=None
    ):

        body = {
            "text": text,
            "attachments": attachments if attachments is not None else []
        }

        response = requests.put(
            self.base_url + "/messages",
            headers=self.headers,
            params={"message_id": message_id},
            json=body,
            verify=self.verify_ssl
        )

        response.raise_for_status()

        return response.json()

    def set_commands(self, commands: list[dict]):

        body = {
            "commands": commands
        }

        response = requests.patch(
            self.base_url + "/me/commands",
            headers=self.headers,
            json=body,
            verify=self.verify_ssl
        )

        response.raise_for_status()

        return response.json()