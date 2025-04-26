import socket
import threading

# Server network handler
class SeverNetworkHandler:
    
    # Server side initialization
    def __init__(self, host='0.0.0.0', port=6001):
        self.host = host
        self.port = port
        self.server_socket = None
        self.connection = None
        self.address = None
        self.running = False

    # Server side sever start
    def start_server(self):
        
        # Create socket
        self.server_socket = socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind
        self.server_socket.bind((self.host, self.port))
        
        # Listen
        self.server_socket.listen(1)
        
        # Debug
        print(f"Server listening on {self.host}:{self.port}")
       
        self.running = True

        # Start accepting connections in a new thread
        threading.Thread(target=self.accept_connection, daemon=True).start()

    # Accepting connection from client
    def accept_connection(self):
        try:
            self.connection, self.address = self.server_socket.accept()
            print(f"Accepted connection from {self.address}")

            # Start a thread to handle receiving data
            threading.Thread(target=self.receive_loop, daemon=True).start()
        except Exception as e:
            print(f"Error accepting connection: {e}")

    # Server recieves
    def receive_loop(self):
        while self.running:
            try:
                data = self.connection.recv(4096)
                if data:
                    print(f"Received: {data}")
                    # Here you would decrypt and forward to GUI
                else:
                    print("Connection closed by client.")
                    self.running = False
                    break
            except Exception as e:
                print(f"Receive error: {e}")
                self.running = False
                break
    
    # Server sends
    def send(self, data):
        if self.connection:
            self.connection.sendall(data)

    # Shutdown server
    def shutdown(self):
        self.running = False
        if self.connection:
            self.connection.close()
        if self.server_socket:
            self.server_socket.close()
        print("Server shutdown complete.")



# Client network handler
class ClientNetworkHandler:
    
    # Client side initialization
    def __init__(self, server_ip, server_port=6001):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.running = False

    # Client side sever start
    def start_client(self):
        
        # Create socket
        self.client_socket = socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Client connect to server
        self.client_socket.connect((self.server_ip, self.server_port))
        
        # Debug
        print(f"Connected to server at {self.server_ip}:{self.server_port}")

        self.running = True
        threading.Thread(target=self.receive_loop, daemon=True).start()
        
        self.running = True

        # Start accepting connections in a new thread
        threading.Thread(target=self.receive_loop, daemon=True).start()

    # Client recieves data
    def receive_loop(self):
        while self.running:
            try:
                data = self.client_socket.recv(4096)
                if data:
                    print(f"Received: {data}")
                else:
                    print("Server closed connection.")
                    self.running = False
            except Exception as e:
                print(f"Receive error: {e}")
                self.running = False

    # Client sends data
    def send(self, data):
        if self.client_socket:
            self.client_socket.sendall(data)

    # Shutdown client
    def shutdown(self):
        self.running = False
        if self.connection:
            self.connection.close()
        if self.server_socket:
            self.server_socket.close()
        print("Server shutdown complete.")