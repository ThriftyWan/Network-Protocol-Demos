from src.dns import lookup
from src.ping import ping
from src.traceroute import traceroute

import sys

lookup("example.com")

command = sys.argv[1] if len(sys.argv) > 1 else None
target = sys.argv[2] if len(sys.argv) > 2 else None

if command == "dns":
    lookup(target)
elif command == "ping":
    ping(target)
elif command == "trace":
    traceroute(target)
else:
    print("usage: python main.py <dns|ping|trace> <target>")