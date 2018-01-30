#!/usr/bin/env python3

import serial
import input_messages
import time
from common import port, baudrate

msgs = [
    input_messages.QueryDatumMessage(),
    input_messages.ConfigureDatumMessage(datum_index=0, permanent=True),
    input_messages.QueryDatumMessage(),
]

with serial.Serial(
    port=port,
    baudrate=baudrate
) as ser:
    for msg in msgs:
        print(msg)
        ser.write(bytes(msg))
        time.sleep(1)
