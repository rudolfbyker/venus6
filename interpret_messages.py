#!/usr/bin/env python3

import serial
from output_messages import OutputMessage
from common import line_separator, port, baudrate


def lines():
    with serial.Serial(
        port=port,
        baudrate=baudrate
    ) as ser:
        try:
            while True:
                line = b''
                while len(line) < 2 or line[-2:] != line_separator:
                    line += ser.read(1)
                if line[0] != b'$'[0]:
                    yield line
        except KeyboardInterrupt:
            return


for l in lines():
    try:
        m = OutputMessage(l)
        try:
            print(m.interpret())
        except ValueError:
            print("Failed to interpret message:", m)
    except ValueError:
        print("Failed to interpret line:", l)
