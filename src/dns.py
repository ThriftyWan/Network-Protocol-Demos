import socket
import struct
import random

def encode_hostname(hostname):
    '''
    Encodes a domain name (example.com) into label format
    (b'\x07example\x03com\x00')
    '''
    encoded = b""
    for part in hostname.split("."):
        encoded += bytes([len(part)]) + part.encode()
    encoded += b"\x00"
    return encoded

def build_query(hostname):
    transaction_id = random.randint(0, 65535)
    flags = 0x0100
    qdcount = 1
    ancount = nscount = arcount = 0

    header = struct.pack(">HHHHHH",
        transaction_id,
        flags,
        qdcount,
        ancount,
        nscount,
        arcount
    )

    question = encode_hostname(hostname)
    question += struct.pack(">HH", 1, 1) #QTYPE=A (1), QCLASS=IN (1)

    return header + question, transaction_id

def send_query(packet, server="8.8.8.8"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    sock.sendto(packet, (server, 53))
    response, _ = sock.recvfrom(512)
    sock.close()
    return response

def parse_response(response, transaction_id):
    #Unpack the 12 byte header
    tid, flags, qdcount, ancount, nscount, arcount = struct.unpack(">HHHHHH", response[:12])

    if tid != transaction_id:
        print("Transaction ID mismatch!")
        return
    
    print(f"Got {ancount} answer(s)")

    #Skip past the header and question section
    offset = 12
    while response[offset] != 0:
        offset += 1 + response[offset]
    offset += 5 #Skip null byte + QTYPE + QCLASS

    #Parse each answer
    for _ in range(ancount):
        #Name field - might be a pointer (starting with 0xC0)
        if response[offset] == 0xC0:
            offset += 2 #Pointer is 2 bytes
        else:
            while response[offset] != 0:
                offset += 1 + response[offset]
            offset += 1

        rtype, rclass, ttl, rdlength = struct.unpack(">HHIH", response[offset:offset+10])
        offset += 10

        if rtype == 1 and rdlength == 4:
            ip = socket.inet_ntoa(response[offset:offset+4])
            print(f"   A record: {ip}")

        offset += rdlength

def lookup(hostname, server="8.8.8.8"):
    print(f"Looking up {hostname} using {server}...")
    packet, tid = build_query(hostname)
    response = send_query(packet, server)
    parse_response(response, tid)