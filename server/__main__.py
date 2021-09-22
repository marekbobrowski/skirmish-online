from .server import Server
import time


if __name__ == "__main__":
    server = Server()
    server.run()

    while True:
        time.sleep(10)
