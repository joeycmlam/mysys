import socket
import logging
import sys

class MCPClient:
    def __init__(self, host: str = 'localhost', port: int = 5000):
        self.host = host
        self.port = port
        self.client_socket = None
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('MCPClient')
    
    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.logger.info(f"Connected to MCP Server at {self.host}:{self.port}")
            return True
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False
    
    def send_message(self, message: str) -> str:
        try:
            self.client_socket.send(message.encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')
            self.logger.info(f"Received response: {response}")
            return response
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return None
    
    def close(self):
        if self.client_socket:
            self.client_socket.close()
            self.logger.info("Connection closed")

def main():
    client = MCPClient()
    if client.connect():
        try:
            while True:
                message = input("Enter message (or 'quit' to exit): ")
                if message.lower() == 'quit':
                    break
                client.send_message(message)
        finally:
            client.close()

if __name__ == "__main__":
    main() 