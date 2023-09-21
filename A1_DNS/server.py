import socket
import argparse
import dnslib
from dnslib import DNSRecord, RR, A, DNSHeader, QTYPE

# Define the IP address and port for the DNS server
LOCAL_DNS_SERVER = '127.0.0.1'
LOCAL_DNS_PORT = 1234
PUBLIC_DNS_SERVERS = {'international':'8.8.8.8', 'domeestic':'223.5.5.5'}
ROOT_DNS_SERVERS = ['198.41.0.4', '	199.9.14.201', '192.33.4.12', '199.7.91.13'] # A list of root DNS servers
REMOTE_DNS_PORT = 53  # DNS default port

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=int, default=1, choices=[0, 1], help='Server Mode, 0 for query public server; 1 for iterative query')
    parser.add_argument('-p', '--port', type=int, default=1234, help='Port number')
    return parser.parse_args()

def extract_cnames_and_ips(record: DNSRecord):
    cnames_and_ips = []

    for rr in record.rr:
        rtype = dnslib.QTYPE[rr.rtype]
        if rtype == 'CNAME':
            cnames_and_ips.append((str(rr.rname), str(rr.rdata.label)))

        elif rtype in ['A', 'AAAA']:
            # Extract A or AAAA records
            cnames_and_ips[-1] = (cnames_and_ips[-1][0], str(rr.rdata))

    return cnames_and_ips

def _query(socket, query, dns_server_ip):
    socket.sendto(query.pack(), (dns_server_ip, REMOTE_DNS_PORT))
    respond_data, _ = socket.recvfrom(1024)
    response = DNSRecord.parse(respond_data)
    dns_dict = map_auth_name_to_ip(response)
    return response, dns_dict

def handle_dns_request(data, mode=0):
    request = DNSRecord.parse(data)
    query_domain = str(request.q.qname)
    print(f"Query Domain: {query_domain}")
    if mode == 0:
        public_dns_ip = PUBLIC_DNS_SERVERS.get('international', '8.8.8.8')
        public_dns_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            public_dns_sock.sendto(data, (public_dns_ip, REMOTE_DNS_PORT))
            public_response_data, _ = public_dns_sock.recvfrom(1024)
            response = DNSRecord.parse(public_response_data)
        except Exception as e:
            print(f"Error while querying public DNS server: {e}")
        finally:
            public_dns_sock.close()
    else:
        response = iterative_query(data, ROOT_DNS_SERVERS)

    return response.pack()

get_client_request_meta = lambda request: (str(request.q.qname), str(request.q.qtype))

def map_auth_name_to_ip(record: DNSRecord):
    auth_dict = {}
    for rr in record.auth:
        auth_dict[str(rr.rdata)] = None
    for ar in record.ar:
        if str(ar.rname) in auth_dict and ar.rtype == QTYPE.A:
            auth_dict[str(ar.rname)] = str(ar.rdata)
    return auth_dict

def main(args):
    # Create a UDP socket for DNS server
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock.bind((LOCAL_DNS_SERVER, LOCAL_DNS_PORT))
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"DNS server is listening on {LOCAL_DNS_SERVER}:{LOCAL_DNS_PORT}")

    while True:
        data, addr = client_sock.recvfrom(1024)
        query_url = str(DNSRecord.parse(data).q.qname)
        print(f"Received DNS request from {addr[0]}:{addr[1]}")

        query = DNSRecord.parse(data)
        # domain, qtype = get_client_request_meta(response)
        
        query_dns_server = ROOT_DNS_SERVERS[0]
        while True:
            response, dns_dict = _query(server_sock, query, query_dns_server)
            if response.a.rdata is not None:
                break
            for dns_server_name, dns_server_ip in dns_dict.items():
                if dns_server_ip is not None:
                    query_dns_server = dns_server_ip
                    break
        print(str(response))
        client_sock.sendto(data, addr)
    server_sock.close()
    client_sock.close()


if __name__ == '__main__':
    args = parse_args()
    main(args)