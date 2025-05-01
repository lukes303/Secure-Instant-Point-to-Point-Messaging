import socket
import threading
from Cryptography import Cryptography
# from logging import config
from time import sleep

# Global variables
server_socket = None
client_socket = None
listening = False
peer_ip = None
mode = None
password = None
ip_address = None
port = 12000  # Default port

# Encryption
crypto = None

# For tracking connected clients (if server)
clients = []

# Message history
message_history = []

def initialize_app(user_config):
    """Initialize the app with the user configuration"""
    global mode, password, ip_address, crypto
    mode = 'client' if user_config.get("mode") == 0 else 'server'
    password = user_config.get("password")
    ip_address = user_config.get("ip") if mode == 'client' else get_local_ip()
    
    # Initialize the encryption
    crypto = Cryptography()
    crypto.initialize(password)

def get_local_ip():
    """Get local IP address for server mode"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def start_server():
    """Start the server (if not already started)"""
    global server_socket, listening
    if not listening:  # Prevent multiple server instances
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip_address, port))
        server_socket.listen(5)  # Allow up to 5 clients
        listening = True
        print(f"Server started on {ip_address}:{port}")
        threading.Thread(target=accept_connections, daemon=True).start()
    else:
        print("Server is already running.")

def start_client():
    """Connect the client to the server, start server if needed"""
    global client_socket, peer_ip
    try:
        # Attempt to connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, port))
        peer_ip = ip_address
        print(f"Connected to server at {peer_ip}:{port}")
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    except ConnectionRefusedError:
        print("Server is not running, starting the server now...")
        # If connection failed, start the server and retry connecting
        start_server()
        sleep(1)  # Wait a moment to ensure the server has started
        # Now try to connect the client again
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, port))
        peer_ip = ip_address
        print(f"Connected to server at {peer_ip}:{port}")
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

def start_network():
    """Start network based on mode (server or client)"""
    if mode == 'server':
        start_server()
    else:
        start_client()

def accept_connections():
    """Accept incoming connections (server mode)"""
    global server_socket, client_socket, peer_ip
    while listening:
        conn_socket, addr = server_socket.accept()
        # When a client connects, assign the connection socket and peer IP
        client_socket = conn_socket
        peer_ip = addr[0]
        clients.append(conn_socket)  # Add this client to the list of clients
        print(f"Client {peer_ip} connected.")
        threading.Thread(target=receive_messages, args=(conn_socket,), daemon=True).start()

def receive_messages(client_socket):
    while True:
        try:
            encrypted_msg = client_socket.recv(1024).decode()
            if not encrypted_msg:
                break
            plaintext = crypto.decrypt(encrypted_msg)
            message_history.append({
                'type': 'received',
                'ciphertext': encrypted_msg,
                'plaintext': plaintext,
                'from': peer_ip
            })
        except ConnectionError:
            print("⚠️ Connection lost.")
            break

    client_socket.close()
    client_socket = None  # This sets the global client_socket to None


def send_message(plaintext):
    """Encrypt and send a message"""
    global client_socket, peer_ip
    if not client_socket:
        return False
        
    encrypted_msg = crypto.encrypt(plaintext)
    try:
        client_socket.send(encrypted_msg.encode())
    except (BrokenPipeError, OSError):
        print("Error: Connection is broken. Cannot send.")
        return False
    
    # Add to message history
    message_history.append({
        'type': 'sent',
        'ciphertext': encrypted_msg,
        'plaintext': plaintext,
        'to': peer_ip
    })
    
    return True

def disconnect():
    """Clean up network connections"""
    global server_socket, client_socket, listening
    if client_socket:
        client_socket.close()
    if server_socket:
        server_socket.close()
    listening = False
    print("Connection closed.")
