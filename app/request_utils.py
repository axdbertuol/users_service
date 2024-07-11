import aiohttp
from xeez_pyutils.exceptions import InternalServerError, NotFoundError


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def post_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            try:
                response.raise_for_status()
                json_res = await response.json()
                return json_res
            except Exception as e:
                raise InternalServerError("Something went wrong during post request", e)
