from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    trello_api_key: str
    trello_api_token: str
    trello_board_id: str
    discord_api_token: str
    discord_channel_id: str
    check_interval: int = 60

    class Config:
        env_file = "../.env"
