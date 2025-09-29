import time

import zmq
from pmr_elirobots_msgs.cmd import Command, CommandMsg
from pmr_elirobots_msgs.types import ClawState


class Client:
    def __init__(self, ip: str = "localhost", port: int = 5555, topic: str = "cmd"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.connect(f"tcp://{ip}:{port}")
        self.topic = topic.encode("utf-8")

    def send_command(
        self,
        *,
        joint1: float | None = None,
        joint2: float | None = None,
        joint3: float | None = None,
        joint4: float | None = None,
        joint5: float | None = None,
        joint6: float | None = None,
        claw: ClawState | None = None,
    ):
        msg = CommandMsg()
        msg.cmd = Command(
            joint1=joint1,
            joint2=joint2,
            joint3=joint3,
            joint4=joint4,
            joint5=joint5,
            joint6=joint6,
            claw=claw,
        )

        self.socket.send_multipart([self.topic, msg.to_json().encode("utf-8")])


if __name__ == "__main__":
    robot = Client()

    count = 0
    while True:
        count += 1

        if count % 2:
            print("Send cmd1")
            robot.send_command(
                joint1=180, joint2=0, joint3=0, joint4=0, joint5=0, joint6=0, claw=ClawState.OPEN
            )
        else:
            print("Send cmd2")
            robot.send_command(joint2=-90, claw=ClawState.CLOSE)

        time.sleep(10)
