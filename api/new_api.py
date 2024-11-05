from socket import *
import json
import api.info_api as info_api
import threading

BUFFER_SIZE = 4096

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    source: https://refactoring.guru/design-patterns/singleton/python/example
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Api(metaclass=SingletonMeta):
    def __init__(self, address, port):
        
        self.address = address
        self.port = port

        self.client = None

        # self.last_data_sent = {}

    # Initiate socket connection
    def start(self):
        self.obj_socket = socket(AF_INET, SOCK_STREAM)
        self.obj_socket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        # Bind the socket to the port
        server_address = (self.address, self.port)
        self.obj_socket.bind(server_address)
        print ("Starting API...")

        # Listen to clients, argument specifies the max no. of queued connections
        self.obj_socket.listen(1)
        self.client, self.client_address = self.obj_socket.accept()
        # print("Connection initiated with client: ", self.client_address)
    
    # Sends dict game data to socket listener
    def send_data(self, Info_api):
        data_dict = Info_api.organize_send()
        msg = json.dumps(data_dict)
        if self.client:
            self.obj_socket.sendall(msg.encode())
    
    def send_custom_data(self, data):
        msg = json.dumps(data)
        if self.client:
            self.obj_socket.sendall(msg.encode())
