import aiohttp

class Parser:
    def __init__(self):
        pass

    @staticmethod
    async def request (url, payload = None, header = None) :
        async with aiohttp.ClientSession (headers=header) as session :
            async with session.get (url=url, params=payload) as r :
                data = await r.text()
        return data

    @staticmethod
    async def post (url, payload = None, header = None) :
        async with aiohttp.ClientSession (headers=header) as session :
            async with session.post (url=url, params=payload) as r :
                data = await r.text()
        return data