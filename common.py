
byteorder = 'big'
port = '/dev/ttyAMA0'
baudrate = 115200


def read_lines(ser, line_separator=b'\r\n', max_length=100):
    """

    :param Serial ser: The serial interface. Has to have a read method which returns bytes.

    :param line_separator: The characters to look for to determine the end of a line. They will not be stripped or
    converted.

    :param max_length: Stop if the line gets longer than this number of bytes. NMEA messages should always be at most
    82 characters long, so 100 is a safe threshold. This helps to detect endless streams of garbage.

    :return: Generator that yields one line at a time.

    """
    while True:
        line = b''
        while not line.endswith(line_separator):
            new_byte = ser.read(1)
            if len(new_byte) != 1:
                raise TimeoutError("UART Timeout")
            line += new_byte
            if len(line) > max_length:
                raise TimeoutError("UART line longer than {} bytes. Maybe the baud rate is wrong?".format(max_length))
        yield line


def read_lines_ignoring_timeouts(ser, line_separator=b'\r\n', max_length=100, max_timeouts=2):
    n_timeouts = 0
    while n_timeouts < max_timeouts:
        try:
            for line in read_lines(ser=ser, line_separator=line_separator, max_length=max_length):
                yield line
        except TimeoutError as e:
            n_timeouts += 1
            print("Timeout {} of {}: {}".format(
                n_timeouts,
                max_timeouts,
                e
            ))
    raise TimeoutError("Maximum number of timeouts reached.")


def interpret_messages(lines, skip_nmea=False):
    from output_messages import OutputMessage
    from messages import NmeaMessage

    for line in lines:
        if line.startswith(b'$'):
            if skip_nmea:
                continue
            else:
                yield NmeaMessage(line)
        else:
            try:
                msg = OutputMessage(line)
                try:
                    yield msg.interpret()
                except ValueError:
                    yield msg
            except ValueError:
                print("Failed to interpret line:", line)
    print("interpret_messages for loop completed")


def look_for_ack(messages, msg_id, limit=5):
    from output_messages import NackMessage, AckMessage

    for i, m in enumerate(messages):
        print(m)
        if type(m) is NackMessage:
            raise RuntimeError("Got NACK")
        if type(m) is AckMessage and m.values[0].value == msg_id:
            return i  # we got our ACK
        if i > limit:
            raise TimeoutError("No ACK after {} messages.".format(limit))
    raise RuntimeError("No ACK found in messages.")


def detect_baudrate(serial_port):
    import serial
    from input_messages import QuerySoftwareVersionMessage
    from fields import BaudRateField

    out_msg = QuerySoftwareVersionMessage(1)
    for i_br in BaudRateField.allowed_values:
        br = BaudRateField.allowed_values[i_br]
        print("Trying {} bps...".format(br))
        with serial.Serial(port=serial_port, baudrate=br, timeout=1) as ser:
            print("Probing software version...")
            ser.write(bytes(out_msg))
            print("Waiting for ACK...")
            try:
                i_ackmsg = look_for_ack(
                    messages=interpret_messages(read_lines_ignoring_timeouts(ser)),
                    msg_id=QuerySoftwareVersionMessage.msg_id
                )
                print("Got ACK after {} messages.".format(i_ackmsg))
                return i_br, br
            except TimeoutError as e:
                print("Timeout: {}".format(e))
                continue
    raise RuntimeError("Failed to determine baud rate")
