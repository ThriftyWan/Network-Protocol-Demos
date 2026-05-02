import socket
import threading

#This lock prevents multiple threads printing at the same time and garbling output
print_lock = threading.Lock()
open_ports = []

def scan_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            with print_lock:
                print(f" [OPEN] port {port}")
            open_ports.append(port)
    
    except socket.error:
        pass

def scan_range(host, start_port=1, end_port=1024):
    print(f"Scanning {host} ports {start_port}-{end_port}...\n")

    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(host, port))
        threads.append(t)
        t.start()

    #Wait for all threads to finish
    for t in threads:
        t.join()
    
    print(f"\nDone. Fouind {len(open_ports)} open port(s).")