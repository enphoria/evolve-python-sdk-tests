import asyncio

from zepben.evolve.streaming import connect, connect_async, NetworkConsumerClient
from zepben.evolve import NetworkService, SyncNetworkConsumerClient, Equipment


async def main():
    async with connect_async(host="localhost", rpc_port=50052) as channel:
        service = NetworkService()
        client = NetworkConsumerClient(channel)
        result = (await client.get_feeder(service, '55832b20-0dd2-404e-bce6-61734a025d77')).throw_on_error()
        print(service.get('55832b20-0dd2-404e-bce6-61734a025d77'))

        for equip in service.objects(Equipment):
            print(equip.mrid, equip.name)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
