'''
Author: tianhao 120090472@link.cuhk.edu.cn
Date: 2023-09-23 23:11:56
LastEditors: tianhao 120090472@link.cuhk.edu.cn
LastEditTime: 2023-10-15 21:33:40
FilePath: /A1_DNS/server.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import time
import socket
import argparse
from dnslib import DNSRecord, QTYPE

LOCAL_DNS_SERVER = '127.0.0.1'
LOCAL_DNS_PORT = 1234
PUBLIC_DNS_SERVER = '223.5.5.5' # AliDNS
ROOT_DNS_SERVER = '198.41.0.4'  # Root DNS A

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--flag', type=int, default=1, choices=[0, 1], help='Server Mode, 0 for query public server; 1 for iterative query')
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
    return str(reply.auth[0].rdata), str(reply.auth[0].rdata)

def try_send_request(request, server_name, trials=10):
    trial = 0
    timeout = 0.5
    while trial < trials:
        try:
            return request.send(server_name, timeout=timeout)
        except socket.timeout:
            trial += 1
            time.sleep(timeout)

def get_ip_from_url(domain_name:str, flag:int):
    global passed_server
    server_name = ROOT_DNS_SERVER if flag==1 else PUBLIC_DNS_SERVER
    server_ip = server_name
    while True:
        request = DNSRecord.question(domain_name)
        passed_server.append(server_ip)
        raw_reply = try_send_request(request, server_name)
        reply = DNSRecord.parse(raw_reply)
        if (reply.auth != []):
            server_name, _server_ip = get_nameserver_info(reply)
            server_ip = _server_ip
        if (reply.rr != []):
            reply_rr = (reply.rr).copy()
            _cname_rr = None # usually there won't be two cname records
            is_cname = True
            for rr in reply_rr:
                if rr.rtype == QTYPE.CNAME:
                    _cname_rr = rr
                elif rr.rtype == QTYPE.A:
                    is_cname = False
                    break
            if is_cname:
                _reply = get_ip_from_url(str(_cname_rr.rdata), flag)
                reply.rr += _reply.rr
            return reply

def main(args):
    global passed_server
    cache = {}
    while True:
        passed_server = []
        data, addr = client_sock.recvfrom(1024)
        query = DNSRecord.parse(data)
        query_url = str(query.q.qname)
        if query_url in cache:
            final_msg = query.reply()
            final_msg.rr = cache[query_url]
        else:
            reply = get_ip_from_url(query_url, args.flag)
            final_msg = query.reply()
            final_msg.rr = reply.rr
            cache[query_url] = final_msg.rr
        print_passed_servers(passed_server)
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