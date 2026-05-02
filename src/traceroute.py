from scapy.all import IP, ICMP, sr1
import socket

def traceroute(host):
    dest = socket.gethostbyname(host)
    print(f"Traceroute to {host} ({dest}), max 30 hops\n")

    for ttl in range(1, 31):
        packet = IP(dst=dest, ttl=ttl) / ICMP()

        reply = sr1(packet, verbose=0, timeout=3)

        if reply is None:
            print(f"  {ttl:2d}  * * *  (no reply)")
            continue

        router_ip = reply.src

        try:
            hostname = socket.gethostbyaddr(router_ip)[0]
            print(f"  {ttl:2d}  {hostname} ({router_ip})")
        except socket.herror:
            print(f"  {ttl:2d}  {router_ip}")

        if router_ip == dest:
            print("\nReached destination.")
            break