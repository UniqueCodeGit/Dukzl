from utils.parser import Parser
from bs4 import BeautifulSoup

class Instagram:
    def __init__(self): pass

    @staticmethod
    async def DownloadOneImage (code : str):
        url = f"https://www.instagram.com/p/{code}/"
        data = await Parser.request(url = url)
        soup = BeautifulSoup(data,'html.parser')
        image = soup.find_all('meta', {'property':'og:image'})
        imgURL = image[0]['content']
        print (image)
        return imgURL
