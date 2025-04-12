from server import MCPServer
import argparse

def main():
    parser = argparse.ArgumentParser(description='MCP Server')
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=5000, help='Server port')
    args = parser.parse_args()

    server = MCPServer(host=args.host, port=args.port)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

if __name__ == "__main__":
    main() 