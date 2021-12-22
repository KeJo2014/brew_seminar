import logging

from communication.websocket import *

def main():
    """
    This method is called when server is started
    """
    logging.info("Pi is starting...")

    # Start the server
    start_server = websockets.serve(server, "localhost", 5000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    logging.info("Program starting...")
    main()