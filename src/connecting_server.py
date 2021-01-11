import asyncio

from zepben.evolve import connect, connect_async, NetworkConsumerClient
from zepben.evolve import NetworkService, SyncNetworkConsumerClient, Equipment


async def main():
    async with connect_async(host="localhost", rpc_port=50052) as channel:
        service = NetworkService()
        client = NetworkConsumerClient(channel)
        result = (await client.get_feeder(service,'basicFeeder_mrid')).throw_on_error()
        print(service.get('basicFeeder_mrid'))

        for equip in service.objects(Equipment):
            print(equip.mrid, equip.name)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
