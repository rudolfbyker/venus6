#!/usr/bin/env python3

import serial
import input_messages
import time
from common import port, baudrate

msgs = [
    input_messages.QueryPositionUpdateRateMessage(),
    input_messages.ConfigurePositionUpdateRateMessage(rate=20, permanent=True),
    input_messages.QueryPositionUpdateRateMessage(),
]

with serial.Serial(
    port=port,
    baudrate=baudrate
) as ser:
    for msg in msgs:
        print(msg)
        ser.write(bytes(msg))
        time.sleep(1)
