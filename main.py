from time import sleep
import requests
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from typing import Final
from datetime import datetime, timezone, time, timedelta

load_dotenv()


class DiscordBot:
    def __init__(self) -> None:
        self.DISCORD_API_TOKEN: Final[str] = os.getenv('Discord_API_Token')


class TrelloReminder:
    def __init__(self) -> None:
        self.TRELLO_API_KEY: Final[str] = os.getenv('Trello_API_Key')
        self.TRELLO_API_TOKEN: Final[str] = os.getenv('Trello_API_Token')

        self.TRELLO_URL_MEMBERS: Final[str] = 'https://api.trello.com/1/boards/sS5WhCA5/members'
        self.TRELLO_URL_CARDS: Final[str] = 'https://api.trello.com/1/boards/sS5WhCA5/cards'

        self.project_users: list[dict[str, str]] = []
        self.project_tasks: list[dict[str, str]] = []

        self.time_alerts: dict[datetime.timedelta, str] = {
            timedelta(days=3): 'You have 3 days left!',
            timedelta(days=1): 'You have 1 day left!',
            timedelta(hours=1): 'You have 1 hour left - dont forget to check off the task!',
        }

    def get_members(self) -> None:
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

    def get_cards_tasks(self) -> None:
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

    def sent_discord_alert(self, id_members: list[str], message: str) -> None:
        print(message)

    def check_tasks_deadline(self):
        for task in self.project_tasks:
            if task['due'] is not None:
                date_now: datetime.datetime = datetime.now(timezone.utc)

                task_due_date: datetime.datetime = datetime.fromisoformat(
                    task['due'].replace("Z", "+00:00")
                )

                task_due_date_left: datetime.timedelta = task_due_date - date_now

                for alert_time, message in self.time_alerts.items():
                    if task_due_date_left <= alert_time:
                        return self.sent_discord_alert(task['idMembers'], message)

if __name__ == "__main__":
    TrelloReminder: TrelloReminder = TrelloReminder()

    TrelloReminder.get_cards_tasks()
    TrelloReminder.get_members()

    while True:
        TrelloReminder.check_tasks_deadline()
        sleep(60)