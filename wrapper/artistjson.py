import json
import os.path

def ConvertName(name):
    name = name.replace(" ", "")
    name = name.lower()
    return name

class DukzlArtist:
    def __init__(self): pass

    @staticmethod
    def MakeArtistJson(artist):
        real_name = ConvertName(artist)
        default_data = {
            "name" : f"{real_name}",
            "real_name" : "",
            "birthday" : "",
            "height" : "",
            "weight" : "",
            "song" : "",
            "instagram" : "",
            "melon" : "",
            "youtube" : "",
            "soundcloud" : "",
            "profilepic" : "",
            "company" : ""
        }
        with open(f"artists/{real_name}.json", "w", encoding="utf-8") as f:
            json.dump(default_data, f)

    @staticmethod
    def CheckExistence(artist):
        real_name = ConvertName(artist)
        if os.path.isfile(f"artists/{real_name}.json"):
            return True
        return False

    @staticmethod
    def EditElement(artist, element, object):
        rn = ConvertName(artist)
        with open(f"artists/{rn}.json", "r") as f:
            ArtistData = json.load(f)
        ArtistData[element] = object
        with open(f"artists/{rn}.json", "w", encoding="utf-8") as f:
            json.dump(ArtistData, f)

    @staticmethod
    def ReturnJson(artist):
        rn = ConvertName(artist)
        with open(f"artists/{rn}.json", "r") as f:
            ArtistData = json.load(f)
        return ArtistData
