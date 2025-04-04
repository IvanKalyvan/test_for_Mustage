import aiohttp

from config import api_url

async def init():

    async with aiohttp.ClientSession() as session:

        yield session

async def post_expenses(endpoint, data):

    async for session in init():

        return await session.post(api_url+endpoint, json=data)

async def get_expenses(endpoint, data):

    async for session in init():

        response = await session.get(api_url+endpoint, params=data)

        return response

async def delete_expenses(endpoint, id):

    async for session in init():

        response = await session.delete(api_url+endpoint, params=id)

        return response

async def update_expenses(endpoint, data):

    async for session in init():

        return await session.patch(api_url+endpoint, json=data)