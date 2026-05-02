from src.dns import lookup
from src.ping import ping
from src.traceroute import traceroute
from src.portscan import scan_range
from src.http_client import http_get

import sys

command = sys.argv[1] if len(sys.argv) > 1 else None
target = sys.argv[2] if len(sys.argv) > 2 else None

if command == "dns":
    lookup(target)
elif command == "ping":
    ping(target)
elif command == "trace":
    traceroute(target)
elif command == "scan":
    scan_range(target)
elif command == "http":
    http_get(target)
else:
    print("usage: python main.py <dns|ping|trace> <target>")