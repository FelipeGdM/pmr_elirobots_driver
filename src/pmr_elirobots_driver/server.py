import zmq
from zmq.eventloop.zmqstream import ZMQStream
# from zmq.eventloop.ioloop import IOLoop
from tornado.ioloop import IOLoop

import random
import time

from rich.live import Live
from rich.table import Table
from rich.console import Console


def generate_table(alive_p1: bool, alive_p2: bool) -> Table:
    table = Table()
    table.add_column("ID")
    table.add_column("Status")

    table.add_row("Player 1", "[red]ERROR" if alive_p1 else "[green]LIVE")
    table.add_row("Player 2", "[red]ERROR" if alive_p2 else "[green]LIVE")

    return table

world_state = {
    "alive_p1": True,
    "alive_p2": True
}

def update_table():
    return generate_table(world_state["alive_p1"], world_state["alive_p2"])

# Create a ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

console = Console()
console.clear()

live = Live(update_table(), console=console, auto_refresh=False)
live.console.clear()
def receive_callback(msg):
    live.console.clear()

    update_table()

    # live.console.print("\n")
    # live.console.print(f"received {msg[0]}")

    live.refresh()
    socket.send(b"World")

# Create a ZMQStream from the socket
stream = ZMQStream(socket)

# Register the callback for incoming messages
stream.on_recv(receive_callback)

# Start the event loop (essential for callbacks to work)
console.print("Starting ZMQStream event loop...")

IOLoop.current().start()
