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
        self.obj_socket.bind((self.address, self.port))

        print("Starting api_recv...")

        while threading.main_thread().is_alive():
            # FIXME: the recvfrom function awaits for the application to receive a package,
            #  If the main thread dies this subthread will stil persist, causing the application
            #  to stay hanging despite the death of the other 2 threads that are no longer running.
            data, origem = self.obj_socket.recvfrom(self.buffer_size)
            decoded_data = json.loads(data.decode())
            # Feedback commands from socket (e.g. an interface)
            #print(decoded_data)

            self.Info_api.update_recv(decoded_data)

            self.decod_data = decoded_data