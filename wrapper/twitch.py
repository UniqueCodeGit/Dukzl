import datetime
import orjson
from utils.parser import Parser
from config import CLIENT_ID, CLIENT_SECRET
from log import Log


class TwitchAPI:
    def __new__(cls):
        cls.logger = Log.defaultLogger("TwitchAPI")
        cls.HTTP = Parser()
        return super().__new__(cls)

    @classmethod
    async def get_twitch_token(cls, scopes: str = None) -> str:
        if scopes:
            scopes = f"&scope={scopes}"
        else:
            scopes = ""

        data = await cls.HTTP.post(
            f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials{scopes}"
        )

        data = orjson.loads(data)
        token = data["access_token"]
        cls.logger.info(f"Token made on {datetime.datetime.now()} : {data}")
        return token

    @classmethod
    async def get_users(cls, id: str):
        token = await cls.get_twitch_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Client-ID": f"{CLIENT_ID}",
        }

        cls.logger.info(f"Helix user requests reported. ID : {id}")
        response = await cls.HTTP.request(
            url=f"https://api.twitch.tv/helix/users?login={id}", header=headers
        )
        return response

    @classmethod
    async def get_streams(cls, id: str):
        token = await cls.get_twitch_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Client-ID": f"{CLIENT_ID}",
        }
        cls.logger.info(f"Helix streams request reported. ID : {id}")
        response = await cls.HTTP.request(
            url=f"https://api.twitch.tv/helix/streams?user_login={id}", header=headers
        )
        return response

    @classmethod
    async def check_streaming(cls, id: str) -> bool:
        response = await cls.get_streams(id)
        response = orjson.loads(response)
        if len(response["data"]) > 0:
            return True
        else:
            return False

    @classmethod
    async def get_game(cls, id: str):
        token = await cls.get_twitch_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Client-ID": f"{CLIENT_ID}",
        }
        cls.logger.info(f"Helix game (find by name) request reported. NAME : {id}")
        response = await cls.HTTP.request(
            url=f"https://api.twitch.tv/helix/games?name={id}", header=headers
        )
        return response

    @classmethod
    async def get_game_byid(cls, id: str):
        token = await cls.get_twitch_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Client-ID": f"{CLIENT_ID}",
        }
        cls.logger.info(f"Helix game (find by id) request reported. ID : {id}")
        response = await cls.HTTP.request(
            url=f"https://api.twitch.tv/helix/games?id={id}", header=headers
        )
        return response