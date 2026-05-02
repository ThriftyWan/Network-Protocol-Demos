import socket

def decode_chunked(data):
    body = b""
    while data:
        #Find the end of the chunk size line
        crlf = data.find(b"\r\n")
        if crlf == -1:
            break

        #Parse the chunk size (in the hex)
        chunk_size = int(data[:crlf], 16)

        #A chunk size of 0 means we're done
        if chunk_size == 0:
            break

        #Extract the chunk data
        start = crlf + 2
        body += data[start:start+chunk_size]

        #Move past this chunk (size line + data + trailing \r\n)
        data = data[start + chunk_size + 2:]

    return body


def http_get(host, path="/"):
    #Step 1: resolve the hostname to an IP
    ip = socket.gethostbyname(host)
    print(f"Connecting to {host} ({ip}) on port 80...\n")

    #Step 2: create a TCP socket and connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((ip, 80))

    #Step 3: build and send the HTTP request
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    sock.sendall(request.encode())

    #Step 4: receive the full response
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk

    sock.close()

    #Step 5: split headers and body
    header_section, _, body = response.partition(b"\r\n\r\n")

    #Step 6: decode chunked transfer encoding if needed
    headers_text = header_section.decode()
    if "Transfer-Encoding: chunked" in headers_text:
        body = decode_chunked(body)

    #Step 7: print the headers
    print("--- HEADERS ---")
    for line in headers_text.split("\r\n"):
        print(f"   {line}")

    #Step 8: print body preview (first 500 chars)
    print("\n--- BODY (first 500 chars) ---")
    print(body.decode(errors="replace")[:500])