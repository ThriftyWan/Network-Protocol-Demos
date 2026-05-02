# PyProbe 🔍

A network diagnostic toolkit built from scratch in Python. PyProbe reimplements classic network utilities at the socket level, demonstrating how DNS, ICMP, and TCP/IP protocols work under the hood.

## Features

| Command | Description | Protocol |
|---|---|---|
| `dns` | Resolve domain names to IP addresses | UDP / DNS |
| `ping` | Measure round-trip latency to a host | ICMP |
| `trace` | Map the route packets take across the internet | ICMP / IP TTL |
| `scan` | *(coming soon)* Scan for open ports on a host | TCP |
| `http` | *(coming soon)* Make raw HTTP requests | TCP / HTTP |

## How it works

Rather than using high-level libraries, PyProbe builds and parses binary packets manually using Python's `socket` and `struct` modules — the same way real network tools work at the OS level.

- **DNS** — constructs a DNS query packet by hand in label-encoded wire format and parses the binary response
- **Ping** — sends raw ICMP echo requests with a manually computed one's complement checksum
- **Traceroute** — exploits the IP TTL field to reveal each router along the path to a destination

## Requirements

- Python 3.8+
- [Scapy](https://scapy.net/) — used for traceroute
- [Npcap](https://npcap.com/) — required on Windows for raw packet capture

```bash
pip install scapy
```

## Usage

> **Note:** `ping` and `trace` require administrator/root privileges due to raw socket usage.

```bash
# DNS lookup
python main.py dns example.com

# Ping a host
python main.py ping 8.8.8.8

# Traceroute to a host
python main.py trace 8.8.8.8
```

## Example output

```
$ python main.py dns example.com
Looking up example.com using 8.8.8.8...
Got 2 answer(s)
  A record: 104.20.23.154
  A record: 172.66.147.243

$ python main.py ping 8.8.8.8
Pinging 8.8.8.8 (8.8.8.8)...
  Reply from 8.8.8.8: seq=1 time=8.4ms
  Reply from 8.8.8.8: seq=2 time=8.3ms
  Reply from 8.8.8.8: seq=3 time=8.2ms
  Reply from 8.8.8.8: seq=4 time=8.7ms

$ python main.py trace 8.8.8.8
Traceroute to 8.8.8.8 (8.8.8.8), max 30 hops
   1  * * *  (no reply)
   2  * * *  (no reply)
   3  ae1-br01.lon1.isp.net (62.253.12.1)
   4  72.14.202.1
  11  dns.google (8.8.8.8)

Reached destination.
```

## Project structure

```
PyProbe/
├── main.py          # Entry point and command routing
└── src/
    ├── dns.py       # DNS resolver (UDP, wire format)
    ├── ping.py      # ICMP pinger (raw sockets)
    ├── traceroute.py # Traceroute (TTL manipulation)
    ├── portscan.py  # Port scanner (TCP) - coming soon
    └── http_client.py # HTTP client (TCP) - coming soon
```

## Concepts covered

- OSI model layers 3, 4, and 7
- Binary packet construction with `struct`
- Network byte order (big-endian)
- Raw sockets vs stream/datagram sockets
- ICMP, UDP, TCP protocols
- DNS wire format and label encoding
- IP TTL and routing
- One's complement checksum algorithm
