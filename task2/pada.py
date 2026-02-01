#!/usr/bin/env python3

import argparse
import socket
from scapy.layers.dns import DNS, DNSQR, DNSRR

def parse_args():
    p = argparse.ArgumentParser(prog='pada', description='Craft and send custom DNS packets')
    p.add_argument('-p','--port', type=int, default=53, help='destination port (default: 53)')
    group = p.add_mutually_exclusive_group()
    group.add_argument('-q','--query', action='store_true', help='send as query (default)')
    group.add_argument('-r','--response', action='store_true', help='send as response')
    p.add_argument('-c','--rcode', type=int, choices=range(0,16), default=0, help='response code (0–15)')
    p.add_argument('-t','--txid', type=int, choices=range(0,65536), help='transaction ID (0–65535)')
    p.add_argument('-i','--ipaddr', help='A record IP to include in answer')
    p.add_argument('-n','--ns', help='NS record name to include')
    p.add_argument('query_name', help='domain to query')
    p.add_argument('dns_server', help='destination IP or hostname')
    return p.parse_args()

def craft_packet(args):
    txid = args.txid if args.txid is not None else 0
    if args.response:
        dns = DNS(id=txid, qr=1, aa=1, ra=1, rcode=args.rcode, qd=DNSQR(qname=args.query_name, qtype='A'))
        if args.ipaddr:
            dns.an = DNSRR(rrname=args.query_name, type='A', rdata=args.ipaddr, ttl=300)
        if args.ns:
            dns.ns = DNSRR(rrname=args.query_name, type='NS', rdata=args.ns, ttl=300)
    else:
        dns = DNS(id=txid, rd=1, qd=DNSQR(qname=args.query_name, qtype='A'))
    return bytes(dns)

def main():
    args = parse_args()
    data = craft_packet(args)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(data, (args.dns_server, args.port))
    finally:
        sock.close()

if __name__ == '__main__':
    main()
