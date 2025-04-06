import requests
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from typing import Final

load_dotenv()


class DiscordBot:
    def __init__(self):
        self.DISCORD_API_TOKEN: Final[str] = os.getenv('Discord_API_Token')


class TrelloReminder:
    def __init__(self):
        self.TRELLO_API_KEY: Final[str] = os.getenv('Trello_API_Key')
        self.TRELLO_API_TOKEN: Final[str] = os.getenv('Trello_API_Token')

        self.TRELLO_URL_MEMBERS: Final[str] = 'https://api.trello.com/1/boards/sS5WhCA5/members'
        self.TRELLO_URL_CARDS: Final[str] = 'https://api.trello.com/1/boards/sS5WhCA5/cards'

        self.project_users: list[dict[str, str]] = []
        self.project_tasks: list[dict[str, str]] = []

    def get_members_id_name(self) -> None:
        headers: dict[str, str] = {
            "Accept": "application/json"
        }

        query: dict[str, str] = {
            'fields': 'id,fullName',
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_API_TOKEN
        }

        response: Response = requests.request(
            "GET",
            self.TRELLO_URL_MEMBERS,
            headers=headers,
            params=query,
        )

        for item in response.json():
            self.project_users.append(item)

    def get_members_tasks_date(self) -> None:
        query: dict[str, str] = {
            'fields': 'name,desc,due,idMembers',
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_API_TOKEN
        }

        response: Response = requests.request(
            "GET",
            self.TRELLO_URL_CARDS,
            params=query,
        )

        for item in response.json():
            if item['due'] is not None:
                for index in range(len(item['due'])):
                    if item['due'][index] == 'T':
                        new_hour: str = str(int(item['due'][index + 1] + item['due'][index + 2]) + 2)
                        new_due: str = item['due'][:index + 1] + new_hour + item['due'][index + 3:]
                        item['due'] = new_due
            self.project_tasks.append(item)

def main():
    client.run(token=token_dc)

if __name__ == "__main__":
    TrelloReminder = TrelloReminder()
    TrelloReminder.get_members_id_name()
    TrelloReminder.get_members_tasks_date()
    print(TrelloReminder.project_tasks)
    # print(TrelloReminder.project_tasks)
    # TrelloReminder.convert_utc_to_cest_time()
    # print(TrelloReminder.project_users)
    # print(TrelloReminder.get_members_tasks_date())
