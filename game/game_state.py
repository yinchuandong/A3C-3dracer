import socket
import numpy as np
import json
import base64
import cPickle
from io import BytesIO
from PIL import Image
from flappy_bird import FlappyBird


HOST, PORT = "localhost", 9999

# test pull mode for flappy bird


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    game = FlappyBird()
    while True:
        data = {
            'state': game.s_t,
            'reward': game.reward,
            'terminal': game.terminal
        }
        data_str = cPickle.dumps(data)
        send_msg(sock, data_str)
        action_id = int(sock.recv(1))
        game.process(action_id)
        game.update()
        if data['terminal']:
            game.reset()
    return


def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = str(len(msg)).zfill(20) + msg
    sended_len = 0
    while sended_len < len(msg):
        left = len(msg) - sended_len
        offset = 8000 if left > 8000 else left
        sock.sendall(msg[sended_len: sended_len + offset])
        sended_len += offset
    return



if __name__ == '__main__':
    main()