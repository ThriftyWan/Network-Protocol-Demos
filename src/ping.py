import socket
import struct
import time
import os

def checksum(data):
    if len(data) % 2 != 0:
        data += b'\x00' #Pad to even length

    total = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i+1]
        total += word

    total = (total >> 16) + (total & 0xFFFF)
    total += (total >> 16)
    return ~total & 0xFFFF

def build_ping(sequence):
    pid = os.getpid() & 0xFFFF
    header = struct.pack(">BBHHH", 8, 0, 0, pid, sequence)
    data = b"networktoolkit"
    raw_checksum = checksum(header + data)
    header = struct.pack(">BBHHH", 8, 0, raw_checksum, pid, sequence)
    return header + data

def ping(host):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.settimeout(3)
    except PermissionError:
        print("Error: ping requirese administrator/root priviliges")
        print("Run with: sudo python main.py   (Linux/Mac) or as Administrator (Windows)")
        return
    
    dest = socket.gethostbyname(host)
    print(f"Pinging {host} ({dest})...")

    for sequence in range(1, 5):
        packet = build_ping(sequence)
        start = time.time()
        sock.sendto(packet, (dest, 0))
    
        try:
            response, addr = sock.recvfrom(1024)
            elapsed = (time.time() - start) * 1000
            #Response includes a 20 byte IP header before the ICMP header
            icmp_data = response[20:]
            recv_type = icmp_data[0]
            if recv_type == 0: #echo reply
                print(f"   Reply from {addr[0]}: seq={sequence} time={elapsed:.1f}ms")
        except socket.timeout:
            print(f"   Request timed out (seq={sequence})")

        time.sleep(1)
    
    sock.close()

