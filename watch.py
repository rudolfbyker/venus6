#!/usr/bin/env python3

import serial
from common import port, baudrate, interpret_messages, read_lines


with serial.Serial(port=port, baudrate=baudrate) as ser:
    for msg in interpret_messages(read_lines(ser), skip_nmea=True):
        print(msg)
