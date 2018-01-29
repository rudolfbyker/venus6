#!/usr/bin/env python3

import serial
import input_messages
import time
from common import port

msgs = [
    input_messages.QueryPositionPinningMessage(),
    input_messages.QueryPositionUpdateRateMessage(),
    input_messages.QuerySoftwareVersionMessage(software_type=0),
    input_messages.QuerySoftwareCrcMessage(),
    input_messages.QueryDatumMessage(),
    input_messages.QueryNavigationModeMessage(),
    input_messages.QueryPpsModeMessage(),
    input_messages.QueryWaasStatusMessage(),
]

with serial.Serial(
    port=port
) as ser:
    for msg in msgs:
        print(msg)
        ser.write(bytes(msg))
        time.sleep(1)
