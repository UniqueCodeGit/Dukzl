import datetime
import aiomysql
import config
import asyncio
import json
import os.path


def ConvertName(name):
    name = name.replace(" ", "")
    name = name.lower()
    return name


class DukzlUsers:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def connect_db(self):
        self.db = await aiomysql.create_pool (
            host=config.DB_IP,
            user=config.DB_USER,
            password=config.DB_PW,
            db="leehi",
            autocommit=True,
            loop=self.loop,
            charset="utf8mb4"
        )
    
    async def RegisterUser(self, user):
        serviceregDate = datetime.datetime.today().strftime("%Y년 %m월 %d일")
        default_data = {
            "name": f"{user.name}",
            "id": user.id,
            "started-date": serviceregDate,
            "artists": [],
            "artistlist": []
        }
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(default_data, f)

    
    async def CheckRegistered(self, user):
        if os.path.isfile(f"users/{user.id}.json"):
            return True
        return False

    @staticmethod
    async def CheckArtistJson(artist):
        rn = ConvertName(artist)
        if os.path.isfile(f"artists/{rn}.json"):
            return True
        return False

    @staticmethod
    async def CheckArtistExists(user, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        converted = ConvertName(artist)
        for artists in UserData["artists"]:
            if artists["identifier"] == converted: return True
        return False

    @staticmethod
    async def AddArtist(user, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        startDate = datetime.datetime.today().strftime("%Y년 %m월 %d일")
        identify = ConvertName(artist)
        default_data = {
            "name": artist,
            "identifier": identify,
            "level": 0,
            "started-date": startDate,
            "playlist": []
        }
        UserData["artists"].append(default_data)
        UserData["artistlist"].append(artist)
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)

    @staticmethod
    async def RemoveArtist(user, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        _ = artist
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if artists["identifier"] == artist:
                UserData["artists"].remove(artists)
        UserData["artistlist"].remove(_)
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)

    @staticmethod
    async def ReturnJson(user):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        return UserData

    @staticmethod
    async def AddPlaylist(user, artist, url):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if artists["identifier"] == artist:
                artists["playlist"].append(url)
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)

    @staticmethod
    async def RemovePlaylist(user, artist, url):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if artists["identifier"] == artist:
                artists["playlist"].remove(url)
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)

    @staticmethod
    async def ResetPlaylist(user, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if artists["identifier"] == artist:
                artists["playlist"] = []
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)

    @staticmethod
    async def ReturnPlaylist(user, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if artists["identifier"] == artist:
                return artists["playlist"]

    @staticmethod
    async def LevelUp(user, amount, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        amount = float(amount)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if artists["identifier"] == artist:
                artists["level"] += amount
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)
