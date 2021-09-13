from .server import Server


if __name__ == "__main__":
    server = Server()
    server.run()
    quit_server = input("Press any key to turn off the server...\n")
