import zepben.cimbend as cim
from zepben.cimbend.streaming.connect import connect_async
import asyncio
import argparse
import logging

# TODO: Support creation of DiagramObjects and add to a Diagram Service such that the can be visualized in the Network Map
# The cimbend libary is generating a error with self.diagram.add_object(do)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ds = cim.DiagramService()
ns = cim.NetworkService()
diagram = cim.Diagram(diagram_style=cim.DiagramStyle.GEOGRAPHIC)
eq = cim.PowerTransformer()
do = cim.DiagramObject(diagram=diagram, identified_object_mrid=eq.mrid,
                       style=cim.DiagramObjectStyle.DIST_TRANSFORMER)
diagram.add_object(do)
ds.add(do)
ds.add(diagram)
ns.add(eq)


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

    # Connect to a local postbox instance using credentials if provided.
    async with connect_async(host=args.server, rpc_port=args.rpc_port, conf_address=args.conf_address,
                             client_id=client_id, client_secret=client_secret, pkey=key, cert=cert, ca=ca) as conn:
        # Send the network to the postbox instance.
        res = await conn.send([ns, ds])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

