import datetime
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

    async def RegisterUser(self, user):
        serviceregDate = datetime.datetime.today().strftime("%Y년 %m월 %d일")
        default_data = {
            "name": f"{user.name}",
            "id": user.id,
            "started-date": serviceregDate,
            "artists": [],
            "artistlist": [],
        }
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(default_data, f)

    def CheckRegistered(self, user):
        return os.path.isfile(f"users/{user.id}.json")

    @staticmethod
    def CheckArtistJson(artist):
        rn = ConvertName(artist)
        return os.path.isfile(f"artists/{rn}.json")

    @staticmethod
    async def CheckArtistExists(user, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        converted = ConvertName(artist)
        for artists in UserData["artists"]:
            if not artists["identifier"] == converted:
                continue

            return True
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
            "playlist": [],
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
            if not artists["identifier"] == artist:
                continue
            
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
            if not artists["identifier"] == artist:
                continue

            artists["playlist"].append(url)
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)

    @staticmethod
    async def RemovePlaylist(user, artist, url):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if not artists["identifier"] == artist:
                continue

            artists["playlist"].remove(url)
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)

    @staticmethod
    async def ResetPlaylist(user, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if not artists["identifier"] == artist:
                continue

            artists["playlist"] = []
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)

    @staticmethod
    async def ReturnPlaylist(user, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if not artists["identifier"] == artist:
                continue

            return artists["playlist"]

    @staticmethod
    async def LevelUp(user, amount, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        amount = float(amount)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if not artists["identifier"] == artist:
                continue

            artists["level"] += amount
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)
