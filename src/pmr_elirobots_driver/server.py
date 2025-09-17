# from loguru import logger
# from logging import Logger
import logging
import random
import time

import zmq
from pmr_elirobots_msgs.cmd import JointCommandMsg
from pmr_elirobots_sdk import EC
from rich.console import Console
from rich.live import Live
from rich.table import Table
from tornado.ioloop import IOLoop, PeriodicCallback
from zmq.eventloop.zmqstream import ZMQStream

world_state = {"alive_p1": False, "alive_p2": False}

robot1 = EC("192.168.1.201")
# robot2 = EC("192.168.1.202", auto_connect=True, enable_log=True)
robot2 = EC("192.168.1.202", auto_connect=False, enable_log=False)


# robot2.robot_servo_on()


def generate_table(alive_p1: bool, alive_p2: bool) -> Table:
    table = Table()

    table.add_column("ID")
    table.add_column("Connection")
    table.add_column("Status")

    table.add_row(
        "Robot 1",
        "[green]LIVE" if hasattr(robot1, "sock_cmd") else "[red]ERROR",
        robot1.state.name,
    )
    table.add_row(
        "Robot 2",
        "[green]LIVE" if hasattr(robot2, "sock_cmd") else "[red]ERROR",
        robot2.state.name,
    )

    return table


def refresh_console(console: Console):
    def func():
        console.clear()
        console.print(generate_table(world_state["alive_p1"], world_state["alive_p2"]))

    return func


def receive_callback(raw_msg: list[bytes]):
    if robot2.state == EC.RobotState.ERROR:
        robot2.robot_servo_on()

    # topic = raw_msg[0].decode("utf-8")
    payload = raw_msg[1].decode("utf-8")

    msg = JointCommandMsg.from_json(payload)
    robot2.move_joint(msg.cmd.as_list, 10, block=False)

    world_state["alive_p2"] = True


def health_check():
    world_state["alive_p1"] = robot1.state  # type: ignore
    world_state["alive_p2"] = robot2.state  # type: ignore


# Create a ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind("tcp://*:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, "cmd")  # Subscribe to a topic

console = Console()
console.clear()

# Create a ZMQStream from the socket
stream = ZMQStream(socket)

# Register the callback for incoming messages
stream.on_recv(receive_callback)

console_update = PeriodicCallback(refresh_console(console), 500)

console_update.start()

IOLoop.current().start()
