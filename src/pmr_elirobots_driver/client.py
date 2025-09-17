import zmq
from pmr_elirobots_msgs.cmd import JointCommand, JointCommandMsg


class Client:
    def __init__(self, ip: str = "localhost", port: int = 5555, topic: str = "cmd"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.connect(f"tcp://{ip}:{port}")
        self.topic = topic.encode("utf-8")

    def send_command(
        self, *, joint1=None, joint2=None, joint3=None, joint4=None, joint5=None, joint6=None
    ):
        msg = JointCommandMsg()
        msg.cmd = JointCommand(
            joint1=joint1, joint2=joint2, joint3=joint3, joint4=joint4, joint5=joint5, joint6=joint6
        )

        self.socket.send_multipart([self.topic, msg.to_json().encode("utf-8")])
