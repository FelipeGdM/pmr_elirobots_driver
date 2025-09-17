import time

import zmq
from pmr_elirobots_msgs.cmd import JointCommand, JointCommandMsg

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")


def recreate_socket():
    socket = context.socket(zmq.PUB)
    # socket.setsockopt(zmq.RCVTIMEO, 1000)  # 100ms timeout for receiving
    socket.connect("tcp://localhost:5555")

    return socket


socket = recreate_socket()

msg1 = JointCommandMsg()

msg1.cmd = JointCommand(joint1=180, joint2=0, joint3=0, joint4=0, joint5=0, joint6=0)

msg2 = JointCommandMsg()

msg2.cmd = JointCommand(joint1=180, joint2=-90, joint3=0, joint4=0, joint5=0, joint6=0)

#  Do 10 requests, waiting each time for a response
request = 0
while True:
    request += 1
    print(f"Sending request {request} …")

    if request % 2 == 0:
        socket.send_multipart([b"cmd", msg1.to_json().encode("utf-8")])
    else:
        socket.send_multipart([b"cmd", msg2.to_json().encode("utf-8")])

    print("Socket msg sent")

    # #  Get the reply.
    # message = None

    # try:
    #     message = socket.recv()
    # except zmq.error.Again:
    #     socket = recreate_socket()
    # else:
    #     print(f"Received reply {request} [ {message.decode('utf-8')} ]")

    time.sleep(10)
