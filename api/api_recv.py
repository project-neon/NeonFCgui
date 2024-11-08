from socket import *
import json
import threading
import struct

class ApiRecv(threading.Thread):
    def __init__(self, match, address, port):
        super(ApiRecv, self).__init__()

        BUFFER_SIZE = 4096

        self.match = match
        self.address = address
        self.port = port
        self.buffer_size = BUFFER_SIZE
        self.decod_data = None   

    def connect_info(self, Info_api):
        self.Info_api = Info_api

    # Receives data
    def run(self):
        self.obj_socket = socket(AF_INET, SOCK_DGRAM)
        self.obj_socket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        # Bind the socket to the port
        server_rcv_address = (self.address, self.port)
        self.obj_socket.bind(server_rcv_address)
        print("Starting api_recv...")

        while True:
            data = self.obj_socket.recv(self.buffer_size)
            if data:
                decoded_data = json.loads(data.decode())
                # Feedback commands from socket (e.g. an interface)
                #print(decoded_data)

                self.Info_api.update_recv(decoded_data)

                self.decod_data = decoded_data
                # print("Data Received: %s", decoded_data)
