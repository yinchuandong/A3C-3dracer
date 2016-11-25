import socket
import sys
import numpy as np
import cPickle
import time
import base64
import json


HOST, PORT = "localhost", 9999
# HOST, PORT = "10.12.185.71", 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def encode_img(filename):
    b64 = base64.encodestring(open(filename, "rb").read())
    return b64


def main():
    img = encode_img('test.png')
    data = {
        'img': img,
        'reward': 0.1
    }
    data = json.dumps(data)

    sock.connect((HOST, PORT))
    send_msg(sock, data)
    received = sock.recv(100)
    sock.close()
    print("Received: {}".format(received))

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
    # size = len(encode_img('test.png'))
    # print size
    # print str(123456).zfill(10)
    main()
    # for i in range(1000):
    #     main()
    #     
        
    # with open('test_0.txt', 'w') as f:
    #     img = encode_img('test.png')
    #     data = {
    #         'img': img,
    #         'reward': 0.1
    #     }
    #     data = json.dumps(data)
    #     f.write(data)

