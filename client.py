import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:

        # POST
        async with session.post(
                'http://127.0.0.1:8080/advert/',
                json={'name': 'advert_3',
                      'description': 'description_3',
                      'owner_name': 'owner_3'}
        ) as response:
            print(await response.json())

#         # GET
#         async with session.get('http://127.0.0.1:8080/advert/2') as response:
#             print(await response.json())

#         # PUT
#         async with session.put(
#                 'http://127.0.0.1:8080/advert/2',
#                 json={'name': 'advert_5',
#                       'description': 'description_5',
#                       'owner_name': 'owner_2'}
#         ) as response:
#             print(await response.json())

#         # DELETE
#         async with session.delete('http://127.0.0.1:8080/advert/3') as response:
#             print(await response.json())

if __name__ == '__main__':
    asyncio.run(main())