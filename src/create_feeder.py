import zepben.evolve as cim
from zepben.evolve.streaming import connect_async, ProducerClient
import asyncio
import argparse
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ns = cim.NetworkService()
acls1 = cim.AcLineSegment(name='acls1')
ec1 = cim.EnergyConsumer(name='ec1')
br1 = cim.Breaker(name='HeadFeeder')

t00 = cim.Terminal(conducting_equipment=br1)
t01 = cim.Terminal(conducting_equipment=br1)
t1 = cim.Terminal(conducting_equipment=acls1)
t2 = cim.Terminal(conducting_equipment=acls1)
t3 = cim.Terminal(conducting_equipment=ec1)

br1.add_terminal(t00)
br1.add_terminal(t01)
acls1.add_terminal(t1)
acls1.add_terminal(t2)
ec1.add_terminal(t3)

ns.add(br1)
ns.add(acls1)
ns.add(ec1)
ns.add(t00)
ns.add(t01)
ns.add(t1)
ns.add(t2)
ns.add(t3)

fdr = cim.Feeder(name='testFeeder', normal_head_terminal=t00)
ns.add(fdr)
ns.connect_terminals(t01, t1)
ns.connect_terminals(t2, t3)


async def main():
    parser = argparse.ArgumentParser(description="Zepben cimbend demo ")
    parser.add_argument('server', help='Host and port of grpc server', metavar="host:port", nargs="?",
                        default="localhost")
    parser.add_argument('--rpc-port', help="The gRPC port for the server", default="50051")
    parser.add_argument('--conf-address', help="The address to retrieve auth configuration from",
                        default="http://localhost/auth")
    parser.add_argument('--client-id', help='Auth0 M2M client id', default="")
    parser.add_argument('--client-secret', help='Auth0 M2M client secret', default="")
    parser.add_argument('--ca', help='CA trust chain', default="")
    parser.add_argument('--cert', help='Signed certificate for your client', default="")
    parser.add_argument('--key', help='Private key for signed cert', default="")
    args = parser.parse_args()
    ca = cert = key = client_id = client_secret = None
    if not args.client_id or not args.client_secret or not args.ca or not args.cert or not args.key:
        logger.warning(
            f"Using an insecure connection as at least one of (--ca, --token, --cert, --key) was not provided.")
    else:
        with open(args.key, 'rb') as f:
            key = f.read()
        with open(args.ca, 'rb') as f:
            ca = f.read()
        with open(args.cert, 'rb') as f:
            cert = f.read()
        client_secret = args.client_secret
        client_id = args.client_id
    # Creates a Network
    network = ns

    # Connect to a local postbox instance using credentials if provided.
    async with connect_async(host=args.server, rpc_port=args.rpc_port, conf_address=args.conf_address,
                             client_id=client_id, client_secret=client_secret, pkey=key, cert=cert, ca=ca) as channel:
        # Send the network to the postbox instance.
        client = ProducerClient(channel)
        # Send the network to the postbox instance.
        res = await client.send([network])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
