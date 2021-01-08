import datetime
import aiomysql
import json
import os.path


def ConvertName(name):
    name = name.replace(" ", "")
    name = name.lower()
    return name


class DukzlUsers:
    def __init__(self):
        pass

    @staticmethod
    def RegisterUser(user):
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

    @staticmethod
    def CheckRegistered(user):
        if os.path.isfile(f"users/{user.id}.json"):
            return True
        return False

    @staticmethod
    def CheckArtistJson(artist):
        rn = ConvertName(artist)
        if os.path.isfile(f"artists/{rn}.json"):
            return True
        return False

    @staticmethod
    def CheckArtistExists(user, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        converted = ConvertName(artist)
        for artists in UserData["artists"]:
            if artists["identifier"] == converted: return True
        return False

    @staticmethod
    def AddArtist(user, artist):
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
    def RemoveArtist(user, artist):
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
    def ReturnJson(user):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        return UserData

    @staticmethod
    def AddPlaylist(user, artist, url):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if artists["identifier"] == artist:
                artists["playlist"].append(url)
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)

    @staticmethod
    def RemovePlaylist(user, artist, url):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if artists["identifier"] == artist:
                artists["playlist"].remove(url)
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)

    @staticmethod
    def ResetPlaylist(user, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if artists["identifier"] == artist:
                artists["playlist"] = []
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)

    @staticmethod
    def ReturnPlaylist(user, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if artists["identifier"] == artist:
                return artists["playlist"]

    @staticmethod
    def LevelUp(user, amount, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        amount = float(amount)
        artist = ConvertName(artist)
        for artists in UserData["artists"]:
            if artists["identifier"] == artist:
                artists["level"] += amount
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)
