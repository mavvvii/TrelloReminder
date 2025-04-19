from datetime import datetime, timezone, timedelta
import os

from aiohttp import ClientSession, ClientConnectionError
from typing import Final
from dotenv import load_dotenv

load_dotenv()
#ToDo repair typing and leter use Protocol
#ToDo refresh data by using async
#ToDo refresh data by using async
#ToDo implement discord alert what i would like to send
#ToDo procces the data that i fetch and would to sned to discord
#ToDo add service errors using try raise except ..`

class TrelloReminder:
    def __init__(self) -> None:
        self.__TRELLO_API_KEY: Final[str] = os.getenv('Trello_API_Key')
        self.__TRELLO_API_TOKEN: Final[str] = os.getenv('Trello_API_Token')

        if not self.trello_api_token:
            raise ValueError('Trello API Token is empty')
        if not self.trello_api_key:
            raise ValueError('Trello API Key is empty')

        _BOARD_ID: str = os.getenv('Trello_Board_ID')

        if not _BOARD_ID:
            raise ValueError('Trello Board ID is empty')

        self._TRELLO_URL_MEMBERS: Final[str] = f'https://api.trello.com/1/boards/{_BOARD_ID}/members'
        self._TRELLO_URL_CARDS: Final[str] = f'https://api.trello.com/1/boards/{_BOARD_ID}/cards'

        self._project_users: list[dict[str, str]] = None
        self._project_tasks: list[dict[str, str | list[str]]] = None

        self._alerts: dict[timedelta, str] = {
            timedelta(hours=1): 'You have 1 hour left - dont forget to check off the task!',
            timedelta(days=1): 'You have 1 day left!',
            timedelta(days=3): 'You have 3 days left!',
        }

    @property
    def trello_api_key(self) -> str:
        return self.__TRELLO_API_KEY

    @property
    def trello_api_token(self) -> str:
        return self.__TRELLO_API_TOKEN

    async def fetch_data(
        self,
        url: str,
        method: str = None,
        *,
        headers: dict[str, str] = None,
        params: dict[str, str] = None
    ) -> list[dict[str, str | dict[str, str]]]:

        async with ClientSession() as session:
            allowed_methods: list[str] = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH']

            bad_requests_status: dict[int, str] = {
                400: 'Bad Request – The request was invalid or cannot be served',
                401: 'Unauthorized – Authentication is required and has failed or has not yet been provided',
                403: 'Forbidden – The server understood the request, but refuses to authorize it',
                404: 'Not Found – The requested resource could not be found',
                405: 'Method Not Allowed – The method is not allowed for the requested URL',
                408: 'Request Timeout – The server timed out waiting for the request',
                429: 'Too Many Requests – You have sent too many requests in a given amount of time',
                500: 'Internal Server Error – An error occurred on the server',
                502: 'Bad Gateway – Invalid response from the upstream server',
                503: 'Service Unavailable – The server is currently unavailable (overloaded or down)',
                504: 'Gateway Timeout – The server did not receive a timely response',
            }

            if method.upper() not in allowed_methods:
                raise ValueError('Method not allowed')

            try:
                async with session.request(method=method, url=url, headers=headers, params=params) as response:
                    if response.status in bad_requests_status:
                        raise ValueError(f'{response.status} - {bad_requests_status[response.status]}')
                    return await response.json()
            except ClientConnectionError as e:
                raise ConnectionError(f"Connection failed: {str(e)}")

    async def get_members(self) -> None:
        headers: dict[str, str] = {
            "Accept": "application/json"
        }

        params: dict[str, str] = {
            'fields': 'id,fullName',
            'key': self.trello_api_key,
            'token': self.trello_api_token
        }

        self._project_users = await self.fetch_data(
            self._TRELLO_URL_MEMBERS,
            method='GET',
            headers=headers,
            params=params,
        )

    async def get_cards_tasks(self) -> None:
        params: dict[str, str] = {
            'fields': 'name,desc,due,idMembers',
            'key': self.trello_api_key,
            'token': self.trello_api_token
        }

        self._project_tasks = await self.fetch_data(
            self._TRELLO_URL_CARDS,
            method='GET',
            params=params,
        )

    async def refresh_data(self) -> None:
        await self.get_members()
        await self.get_cards_tasks()

    async def check_tasks_deadline(self):
        #ToDo repair time and alerts
        @staticmethod
        def task_due_left(task_due: str) -> timedelta:
            date_now: datetime = datetime.now(timezone.utc)
            return datetime.fromisoformat(task_due.replace("Z", "+00:00")) - date_now

        for task in self._project_tasks:
            if task['due'] is not None:
                for alert_time, message in self._alerts.items():
                    if task_due_left(task['due']) <= alert_time and task_due_left(task['due']) > timedelta(0):
                        return task
        return None