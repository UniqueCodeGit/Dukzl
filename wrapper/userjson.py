from collections import defaultdict
import os.path
import json
import datetime
import discord
from discord.user import User


class DukzlUsers:
    def __init__(self): pass

    @staticmethod
    def RegisterUser(user):
        serviceregDate = datetime.datetime.today().strftime("%Y년 %m월 %d일")
        default_data = {
            "name" : f"{user.name}",
            "id" : user.id,
            "started-date" : serviceregDate,
            "artists" : []
        }
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(default_data, f)

    @staticmethod
    def CheckRegistered(user):
        if os.path.isfile(f"users/{user.id}.json"):
            return True
        return False

    @staticmethod
    def CheckArtistExists(user, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        for artists in UserData["artists"]:
            if artists["name"] == artist: return True
        return False


    @staticmethod
    def AddArtist(user, artist):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        startDate = datetime.datetime.today().strftime("%Y년 %m월 %d일")
        default_data = {
            "name" : artist,
            "level" : 0,
            "started-date" : startDate,
            "playlist" : []
        }
        UserData["artists"].append(default_data)
        with open(f"users/{user.id}.json", "w", encoding="utf-8") as f:
            json.dump(UserData, f)

    @staticmethod
    def ReturnJson(user):
        with open(f"users/{user.id}.json", "r") as f:
            UserData = json.load(f)
        return UserData

