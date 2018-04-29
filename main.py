try:
    import usocket as socket
except:
    import socket

try:
    import machine
except:
    print("Executing outside micropython")

CONTENT = b"""\
HTTP/1.0 200 OK
Access-Control-Allow-Origin: *

%s
"""

def parse_req(myrequest):
    """Function to pass the url and return the path"""
    items = myrequest.strip().split(b'\r\n')
    path = ""
    for item in items:
        if b'GET' in item:
            adr = item.split()[1]
            if b'?' in adr: 
                adr, params = adr.split(b'?', 1)
            else:
                params = []
            adr = adr.split(b'/')
            if params:
                param_pairs = [p.split(b'=') for p in  params.split(b'&')]
            else:
                param_pairs = []
    param_dict = {key:value for [key, value] in param_pairs}
    return adr, param_dict

def exec_req(adr, param_dict):
    """Function to execute the request"""
    print("URL:", adr, param_dict)
    if adr[1] == b'write':
        try:
            pin = machine.Pin(int(adr[2]), machine.Pin.OUT)
        except:
            return "Error"
        if adr[3] == b'on':
            pin.on()
            return "Pin {} is on".format(str(adr[2]))
        elif adr[3] == b'off':
            pin.off()
            return "Pin {} is off".format(str(adr[2]))
    return "No Action"
    

def main(micropython_optimize=False):
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", 80)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    counter = 0
    while True:
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        print("Client socket:", client_sock)

        if not micropython_optimize:
            client_stream = client_sock.makefile("rwb")
        else:
            client_stream = client_sock

        print("Request:")
        req = client_stream.readline()
        print(req)
        myrequest = req
        while True:
            h = client_stream.readline()
            if h == b"" or h == b"\r\n":
                break
            print(h)
            myrequest = myrequest + h
        print("----------------------")
        url, param_dict = parse_req(myrequest)
        out = exec_req(url, param_dict)
        #out = "URL: {}, PARAM: {}".format(str(url), str(param_dict))
        client_stream.write(CONTENT % bytes(out, 'utf-8'))

        client_stream.close()
        if not micropython_optimize:
            client_sock.close()
        print()


main()
