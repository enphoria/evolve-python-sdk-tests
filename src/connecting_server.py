from zepben.cimbend.streaming import connect, connect_async, NetworkConsumerClient
from zepben.cimbend import NetworkService, SyncNetworkConsumerClient


with connect(host="localhost", rpc_port=50051) as channel:
    service = NetworkService()
    client = NetworkConsumerClient(channel)
    result = await client.get_feeder(service, "CPM3B3")
    print(service.get("CPM3B3"))