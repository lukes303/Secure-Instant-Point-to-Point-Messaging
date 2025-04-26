import unittest
import time
from NetworkModule import ServerNetworkHandler, ClientNetworkHandler

class TestClientServerInteraction(unittest.TestCase):

    def setUp(self):
        self.server = ServerNetworkHandler(host='127.0.0.1', port=6001)
        self.client = ClientNetworkHandler(server_ip='127.0.0.1', server_port=6001)

        self.server.start_server()
        time.sleep(0.5)  # Let server start listening
        self.client.connect_to_server()
        time.sleep(0.5)  # Let client connect and server accept

    def test_message_exchange(self):
        # Send message from client to server
        test_message = b"Hello Server!"
        self.client.send(test_message)

        time.sleep(0.5)  # Give time for message to be received

        received = self.server.connection.recv(4096)
        self.assertEqual(received, test_message)

        # Optionally: send message back from server to client
        response_message = b"Hello Client!"
        self.server.connection.sendall(response_message)

        received_response = self.client.client_socket.recv(4096)
        self.assertEqual(received_response, response_message)

    def tearDown(self):
        self.client.shutdown()
        self.server.shutdown()

if __name__ == "__main__":
    unittest.main()