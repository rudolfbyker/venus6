#!/usr/bin/env python3

import serial
import input_messages
import time
from common import port, baudrate

msgs = [
    input_messages.QueryPositionPinningMessage(),
    input_messages.ConfigurePositionPinningMessage(enable_position_pinning=False),
    input_messages.QueryPositionPinningMessage(),
]

with serial.Serial(
    port=port,
    baudrate=baudrate
) as ser:
    for msg in msgs:
        print(msg)
        ser.write(bytes(msg))
        time.sleep(1)
