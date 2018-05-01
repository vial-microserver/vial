try:
    import usocket as socket
except:
    import socket

try:
    import machine
    import dht
except:
    print("Executing outside micropython")

CONTENT = b"""\
HTTP/1.0 200 OK
Access-Control-Allow-Origin: *

%s
"""

def parse_req(myrequest):
    """Function to pass the url and return the path"""
    myrequest = str(myrequest)
    items = myrequest.strip().split('\r\n')
    path = ""
    for item in items:
        if 'GET' in item:
            adr = item.split()[1]
            if '?' in adr: 
                adr, params = adr.split('?', 1)
            else:
                params = []
            adr = adr.split('/')
            if params:
                param_pairs = [p.split('=') for p in  params.split('&')]
            else:
                param_pairs = []
    param_dict = {key.lower():value.lower() for [key, value] in param_pairs}
    return adr, param_dict

def exec_req(adr, param_dict):
    """Function to execute the request"""
    print("URL:", adr, param_dict)
    if adr[1] == 'write':
        try:
            pinid = int(adr[2])
            pin = machine.Pin(pinid, machine.Pin.OUT)
        except:
            return "Error"
        if adr[3] == 'on':
            pin.on()
            return "Pin {} is on".format(str(pinid))
        elif adr[3] == 'off':
            pin.off()
            return "Pin {} is off".format(str(pinid))
    elif adr[1] == 'read':
        try:
            pinid = int(adr[2])

            if "pull" in param_dict.keys():
                pull = param_dict["pull"]
            else:
                pull = None

            if pull == "up":
                pull = machine.Pin.PULL_UP
            elif pull == "down":
                pull = machine.Pin.PULL_DOWN
            pin = machine.Pin(pinid, machine.Pin.IN, pull) #todo
            return pin.value()
        except:
            return "Error"
    elif adr[1] == "measure":
        try:
            pinid = int(adr[2])
            d = dht.DHT11(machine.Pin(pinid))
            d.measure()
            return str(d.temperature()) + "," + str(d.humidity())
        except:
            return "Error"

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
    print("Listening, connect your browser to http://<this_host>")

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
        client_stream.write(CONTENT % out)

        client_stream.close()
        if not micropython_optimize:
            client_sock.close()
        print()


main()
