#!/usr/bin/env python3

import serial
from common import detect_baudrate, port, look_for_ack, interpret_messages, read_lines_ignoring_timeouts
from common import baudrate as desired_baudrate
from input_messages import ConfigureSerialPortMessage

i_br, current_baudrate = detect_baudrate(serial_port=port, look_for_ack_limit=50, retries=2)

if current_baudrate == desired_baudrate:
    print("Baudrate is already set to the desired value of {} bps.".format(desired_baudrate))
    exit()

print("Baudrate is set to {} bps, but the desired value is {} bps.".format(current_baudrate, desired_baudrate))

msg = ConfigureSerialPortMessage(rate=desired_baudrate, permanent=True)
with serial.Serial(port=port, baudrate=current_baudrate) as ser:
    print("Setting baudrate to {} bps...".format(desired_baudrate))
    ser.write(bytes(msg))
    print("Waiting for ACK...")
    try:
        i_ackmsg = look_for_ack(
            messages=interpret_messages(read_lines_ignoring_timeouts(ser)),
            msg_id=ConfigureSerialPortMessage.msg_id,
            limit=25,
        )
        print("Got ACK after {} messages.".format(i_ackmsg))
    except TimeoutError:
        print("Timeout.")
