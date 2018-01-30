#!/usr/bin/env python3

import serial
import input_messages
import time
from common import port

msgs = [
    input_messages.ConfigureSerialPortMessage(rate=5, permanent=True)
]

with serial.Serial(
    port=port,
    baudrate=9600
) as ser:
    for msg in msgs:
        print(msg)
        ser.write(bytes(msg))
        time.sleep(1)
