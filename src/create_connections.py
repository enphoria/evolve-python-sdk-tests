import zepben.evolve as cim
import asyncio
import argparse
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ns = cim.NetworkService()
acls1 = cim.AcLineSegment()
acls2 = cim.AcLineSegment()
acls3 = cim.AcLineSegment()
ec1 = cim.EnergyConsumer(name='service_point2550056')
ec2 = cim.EnergyConsumer(name='service_point2601173')
j1 = cim.Junction(name='cubicle113527')
j2 = cim.Junction()

t1 = cim.Terminal(conducting_equipment=j1)  # why I need to associate a Terminal to a ConductingEquipment?
t2 = cim.Terminal(conducting_equipment=acls1)
t3 = cim.Terminal(conducting_equipment=acls1)
t4 = cim.Terminal(conducting_equipment=j2)
t5 = cim.Terminal(conducting_equipment=j2)
t6 = cim.Terminal(conducting_equipment=j2)
t7 = cim.Terminal(conducting_equipment=acls2)
t8 = cim.Terminal(conducting_equipment=acls2)
t9 = cim.Terminal(conducting_equipment=acls3)
t10 = cim.Terminal(conducting_equipment=acls3)
t11 = cim.Terminal(conducting_equipment=ec1)
t12 = cim.Terminal(conducting_equipment=ec2)

j1.add_terminal(t1)  # Why I need to add a Terminal that has been referenced previously?
acls1.add_terminal(t2)
acls1.add_terminal(t3)
j2.add_terminal(t4)
j2.add_terminal(t5)
j2.add_terminal(t6)
acls2.add_terminal(t7)
acls2.add_terminal(t8)
acls3.add_terminal(t9)
acls3.add_terminal(t10)
ec1.add_terminal(t11)
ec2.add_terminal(t12)

ns.add(t1)
ns.add(t2)
ns.add(t3)
ns.add(t4)
ns.add(t5)
ns.add(t6)
ns.add(t7)
ns.add(t8)
ns.add(t9)
ns.add(t10)
ns.add(t11)
ns.add(t12)

ns.add(acls1)
ns.add(acls2)
ns.add(acls3)
ns.add(j1)
ns.add(j2)
ns.add(ec1)
ns.add(ec2)

ns.connect_terminals(t1, t2)
ns.connect_terminals(t3, t4)
ns.connect_terminals(t5, t7)
ns.connect_terminals(t5, t9)
ns.connect_terminals(t8, t11)
ns.connect_terminals(t10, t12)


async def main():
    parser = argparse.ArgumentParser(description="Zepben cimbend demo for geoJSON ingestion")
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
    async with cim.connect_async(host=args.server, rpc_port=args.rpc_port, conf_address=args.conf_address,
                             client_id=client_id, client_secret=client_secret, pkey=key, cert=cert, ca=ca) as channel:
        # Send the network to the postbox instance.
        service = cim.NetworkService()
        client = cim.ProducerClient(channel)
        res = await client.send([network])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
