import asyncio

from zepben.evolve.streaming import connect_async, NetworkConsumerClient
from zepben.evolve import NetworkService, Equipment


async def main():
    async with connect_async(host="localhost", rpc_port=50052) as channel:
        service = NetworkService()
        client = NetworkConsumerClient(channel)
        result = (await client.get_feeder(service, 'CPM3B3')).throw_on_error()
        print(service.get('CPM3B3'))

#        for equip in service.objects(Equipment):
#            print(equip.mrid, equip.name)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
