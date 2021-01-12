import asyncio
import argparse

from zepben.evolve import connect_async, NetworkConsumerClient
from zepben.evolve import NetworkService, ConductingEquipment,  get_connected_equipment



def queue_next_equipment(item, exclude=None):
    connected_equips = get_connected_equipment(item, exclude=exclude)
    return connected_equips


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host and port of grpc server', default="localhost")
    parser.add_argument('--rpc-port', help='The gRPC port for the serve', default="50052")
    parser.add_argument('--feeder-mrid', help='The mRID of the Feeder', default="")
    args = parser.parse_args()

    async with connect_async(host=args.host, rpc_port=args.rpc_port) as channel:
        service = NetworkService()
        client = NetworkConsumerClient(channel)
        await client.get_feeder(service, args.feeder_mrid)
        for eq in service.objects(obj_type=ConductingEquipment):
            print(eq)

        #trace = Traversal(queue_next=queue_next_equipment, start_item=eq, process_queue=LifoQueue(), step_actions=[log])
        #await trace.trace()
        #x = SetPhases()
        #await x.run(service)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
