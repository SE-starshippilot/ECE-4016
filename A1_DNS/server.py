import socket
import argparse
from dnslib import DNSRecord, QTYPE

LOCAL_DNS_SERVER = '127.0.0.1'
LOCAL_DNS_PORT = 1234
PUBLIC_DNS_SERVER = '223.5.5.5' # AliDNS
ROOT_DNS_SERVER = '198.41.0.4'  # Root DNS A

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=int, default=1, choices=[0, 1], help='Server Mode, 0 for query public server; 1 for iterative query')
    return parser.parse_args()

def print_passed_servers(passed_server:list):
    if not(passed_server): print("Fetched IP from cache")
    for idx, ps in enumerate(passed_server, 1):
        print(f'#{idx}: {ps}')
    print('='*20)

def get_nameserver_info(reply:DNSRecord.reply):
    for ar in reply.ar:
        if ar.rtype == QTYPE.A:
            return str(ar.rname), str(ar.rdata)
    return str(reply.auth[0].rdata), None

def get_ip_from_url(domain_name:str, mode=1):
    global passed_server
    server_name = ROOT_DNS_SERVER 
    server_ip = ROOT_DNS_SERVER
    while True:
        request = DNSRecord.question(domain_name)
        passed_server.append(server_ip)
        raw_reply = request.send(server_name)
        reply = DNSRecord.parse(raw_reply)
        if (reply.auth != []):
            server_name, _server_ip = get_nameserver_info(reply)
            if _server_ip: 
                server_ip = _server_ip
            else:
                get_ip_from_url(server_name)
        if (reply.rr != []):
            reply_rr = (reply.rr).copy()
            for rr in reply_rr:
                if rr.rtype == QTYPE.CNAME:
                    _reply = get_ip_from_url(str(rr.rdata))
                    for _rr in _reply.rr:
                        reply.add_answer(_rr)
            break
    return reply

def main(args):
    global passed_server
    cache = {}
    while True:
        data, addr = client_sock.recvfrom(1024)
        query = DNSRecord.parse(data)
        query_url = str(query.q.qname)
        if query_url in cache:
            final_msg = query.reply()
            final_msg.rr = cache[query_url]
        else:
            if args.mode == 0:
                reply = query.send(PUBLIC_DNS_SERVER)
                final_msg = DNSRecord.parse(reply)
                passed_server.append(PUBLIC_DNS_SERVER)
            elif args.mode == 1:
                reply = get_ip_from_url(query_url)
                final_msg = query.reply()
                final_msg.rr = reply.rr
            cache[query_url] = final_msg.rr
        print_passed_servers(passed_server)
        passed_server = []
        client_sock.sendto(final_msg.pack(), addr)

if __name__ == '__main__':
    passed_server = []
    args = parse_args()
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock.bind((LOCAL_DNS_SERVER, LOCAL_DNS_PORT))
    print(f"DNS server is listening on {LOCAL_DNS_SERVER}:{LOCAL_DNS_PORT}")
    try:
        main(args)
    except KeyboardInterrupt:
        print('\nServer is closed')
    finally:
        client_sock.close()