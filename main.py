from datetime import datetime, timezone, timedelta
import os
from time import sleep

import requests
from discord import Intents, Client, Message
from dotenv import load_dotenv
from typing import Final

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
        self.project_tasks: list[dict[str, str | list[str]]] = []

        self.alerts: dict[timedelta, str] = {
            timedelta(hours=1): 'You have 1 hour left - dont forget to check off the task!',
            timedelta(days=1): 'You have 1 day left!',
            timedelta(days=3): 'You have 3 days left!',
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

        self.project_users: list[dict[str, str]] = response.json()

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

        self.project_tasks: list[dict[str, str]] = response.json()

    def sent_discord_alert(self, id_members: list[str], message: str) -> None:
        print(id_members, message)

    def check_tasks_deadline(self):

        @staticmethod
        def task_due_left(task_due: str) -> timedelta:
            date_now: datetime = datetime.now(timezone.utc)
            return datetime.fromisoformat(task_due.replace("Z", "+00:00")) - date_now

        for task in self.project_tasks:
            if task['due'] is not None:
                for alert_time, message in self.alerts.items():
                    if task_due_left(task['due']) <= alert_time and task_due_left(task['due']) > timedelta(0):
                        return self.sent_discord_alert(task['idMembers'], message)


if __name__ == "__main__":
    #Todo fetch data using async ?
    #ToDo get discord id members using api ?
    #ToDo Think about how alert should look, check what i fetch in function get_cards_tasks() and build alert
    #Todo compere discord id to trello id to ping this person that belongs to @Jack You have 1 day left!

    TrelloReminder: TrelloReminder = TrelloReminder()

    while True:
        TrelloReminder.get_cards_tasks()
        TrelloReminder.get_members()
        TrelloReminder.check_tasks_deadline()
        sleep(30)