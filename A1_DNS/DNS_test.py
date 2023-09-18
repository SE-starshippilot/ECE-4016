from dnslib import *
from dnslib.server import *


resolver = BaseResolver()
logger = DNSLogger(prefix=False)
server = DNSServer(resolver,port=1234,address="127.0.0.1",logger=logger)
server.start_thread()
q = DNSRecord.question("google.com")
a = q.send("localhost",1234)

print(DNSRecord.parse(a))