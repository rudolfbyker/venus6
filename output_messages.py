from messages import Message
import fields


class OutputMessage(Message):
    """
    A Message from the GPS unit to the host.
    """

    def __init__(self, input_bytes):
        super().__init__()

        if input_bytes[0] != 0xa0 or input_bytes[1] != 0xa1:
            raise ValueError("Malformed message: Start bytes are wrong.")

        if input_bytes[-1] != 0x0a or input_bytes[-2] != 0x0d:
            raise ValueError("Malformed message: End bytes are wrong.")

        payload_length = int.from_bytes(input_bytes[2:4], byteorder='big', signed=False)
        if len(input_bytes) != payload_length + 7:
            raise ValueError("Malformed message: Message length is wrong.")

        self.payload = input_bytes[4:4 + payload_length]
        if input_bytes[-3] != self.calculate_checksum()[0]:
            raise ValueError("Malformed message: Checksum is wrong.")

    def __str__(self):
        s = "GPS > Host: {}".format(type(self).name)
        for v in self.values:
            s += "\n  {}: {}".format(v.name, v)
        return s

    def get_payload(self):
        return self.payload

    def interpret(self):
        payload = self.get_payload()
        return output_message_types[payload[0]](payload)


class SoftwareVersionMessage(OutputMessage):
    msg_id = 0x80
    name = 'Software Version'
    description = '''
This is a response message which provides the software version of the GPS receiver. This message is sent from the GPS
receiver to host. The example below output the SkyTraq software version as 01.01.01-01.03.14-07.01.18 on System image.
The payload length is 14 bytes.

Structure:
<0xA0,0xA1>< PL><80>< message body><CS><0x0D,0x0A>
'''

    # noinspection PyMissingConstructor
    def __init__(self, payload):
        # Don't call super init.

        if payload[0] != type(self).msg_id:
            raise AttributeError("This is the wrong message class for the given payload. Expected {}, got {}.".format(
                type(self).msg_id,
                payload[0]
            ))

        if len(payload) != 14:
            raise AttributeError("Payload length should be 14.")

        self.payload = payload
        self.values = [
            fields.SoftwareTypeField(payload[1]),
            fields.KernelVersionField(payload[2:6]),
            fields.OdmVersionField(payload[6:10]),
            fields.RevisionField(payload[10:14]),
        ]


class SoftwareCrcMessage(OutputMessage):
    msg_id = 0x81
    name = 'Software CRC'
    description = '''
This is a response message which provides the software CRC of the GPS receiver. This message is sent from the GPS
receiver to host. The payload length is 4 bytes.

Structure:
<0xA0,0xA1>< PL><81>< message body><CS><0x0D,0x0A>
'''
    # fields = [
    #     SoftwareTypeField,
    #     CrcField
    # ]


class AckMessage(OutputMessage):
    msg_id = 0x83
    name = 'ACK'
    description = '''
This is a response message which is an acknowledgement to a request message. The payload length is 2 bytes.

Structure:
<0xA0,0xA1>< PL><83>< message body><CS><0x0D,0x0A>
'''

    # noinspection PyMissingConstructor
    def __init__(self, payload):
        # Don't call super init.

        if payload[0] != type(self).msg_id:
            raise AttributeError("This is the wrong message class for the given payload. Expected {}, got {}.".format(
                type(self).msg_id,
                payload[0]
            ))

        if len(payload) != 2:
            raise AttributeError("Payload length should be 2.")

        self.payload = payload
        self.values = [
            fields.AckIdField(payload[1])
        ]

    def __str__(self):
        from input_messages import input_message_types
        try:
            ack_id = self.values[0].value
            ack_name = input_message_types[ack_id].name
            return "GPS acknowleges '{}' (0x{:02x})".format(ack_name, ack_id)
        except KeyError:
            return "GPS acknowleges '?' (0x{:02x})".format(ack_id)


class NackMessage(OutputMessage):
    msg_id = 0x84
    name = 'NACK'
    description = '''
This is a response message which is a response to an unsuccessful request message. This is used to notify the Host that
the request message has been rejected. The payload length is 2 bytes.

Structure:
<0xA0,0xA1>< PL><84>< message body><CS><0x0D,0x0A>
'''

    # noinspection PyMissingConstructor
    def __init__(self, payload):
        # Don't call super init.

        if payload[0] != type(self).msg_id:
            raise AttributeError("This is the wrong message class for the given payload. Expected {}, got {}.".format(
                type(self).msg_id,
                payload[0]
            ))

        if len(payload) != 2:
            raise AttributeError("Payload length should be 2.")

        self.payload = payload
        self.values = [
            fields.AckIdField(payload[1])
        ]

    def __str__(self):
        from input_messages import input_message_types
        try:
            ack_id = self.values[0].value
            ack_name = input_message_types[ack_id].name
            return "GPS rejects '{}' (0x{:02x})".format(ack_name, ack_id)
        except KeyError:
            return "GPS rejects '?' (0x{:02x})".format(ack_id)


class PositionUpdateRateMessage(OutputMessage):
    msg_id = 0x86
    name = 'Position Update Rate'
    description = '''
This is a response message to QUERY POSITION UPDATE RATE which provides the position update rate of the GPS receiver.
This message is sent from the GPS receiver to host. The payload length is 2 bytes.

Structure:
<0xA0,0xA1>< PL><86>< message body><CS><0x0D,0x0A>
'''

    # noinspection PyMissingConstructor
    def __init__(self, payload):
        # Don't call super init.

        if payload[0] != type(self).msg_id:
            raise AttributeError("This is the wrong message class for the given payload. Expected {}, got {}.".format(
                type(self).msg_id,
                payload[0]
            ))

        if len(payload) != 2:
            raise AttributeError("Payload length should be 2.")

        self.payload = payload
        self.values = [
            fields.UpdateRateField(payload[1])
        ]

    def __str__(self):
        return "GPS update rate is {:d}Hz".format(self.values[0].value)


class GpsEphemerisDataMessage(OutputMessage):
    msg_id = 0xB1
    name = 'TODO'
    description = '''

'''

    # noinspection PyMissingConstructor
    def __init__(self, payload):
        # Don't call super init.

        if payload[0] != type(self).msg_id:
            raise AttributeError("This is the wrong message class for the given payload. Expected {}, got {}.".format(
                type(self).msg_id,
                payload[0]
            ))

        # if len(payload) != :
        #     raise AttributeError("Payload length should be .")

        self.payload = payload
        # self.values = [
        #
        # ]

    def __str__(self):
        return "TODO"
        # return "{}".format(self.values)


class GpsDatumMessage(OutputMessage):
    msg_id = 0xAE
    name = 'GPS datum'
    description = '''
This is a response message which provides the datum information of the GPS receiver. This message is sent from the GPS
receiver to host. The payload length is 3 bytes.

Structure:
<0xA0,0xA1>< PL><AE>< message body><CS><0x0D,0x0A>
'''

    # noinspection PyMissingConstructor
    def __init__(self, payload):
        # Don't call super init.

        if payload[0] != type(self).msg_id:
            raise AttributeError("This is the wrong message class for the given payload. Expected {}, got {}.".format(
                type(self).msg_id,
                payload[0]
            ))

        if len(payload) != 3:
            raise AttributeError("Payload length should be 3.")

        self.payload = payload
        self.values = [
            fields.DatumIndexField(payload[1:3])
        ]


class GpsWaasStatusMessage(OutputMessage):
    msg_id = 0xB3
    name = 'gps waas status'
    description = '''
This is a response message which provides the status of the WAAS receiver. This message is sent from the GPS receiver
to host. The payload length is 2 bytes.

Structure:
<0xA0,0xA1>< PL><B3>< message body><CS><0x0D,0x0A>
'''

    # noinspection PyMissingConstructor
    def __init__(self, payload):
        # Don't call super init.

        if payload[0] != type(self).msg_id:
            raise AttributeError("This is the wrong message class for the given payload. Expected {}, got {}.".format(
                type(self).msg_id,
                payload[0]
            ))

        # if len(payload) != :
        #     raise AttributeError("Payload length should be .")

        self.payload = payload
        # self.values = [
        #
        # ]

    def __str__(self):
        return "TODO"
        # return "{}".format(self.values)


class GpsPositionPinningStatusMessage(OutputMessage):
    msg_id = 0xb4
    name = 'GPS position pinning status'
    description = '''
NOTE: This description is incorrect in the application note.
'''

    # noinspection PyMissingConstructor
    def __init__(self, payload):
        # Don't call super init.

        if payload[0] != type(self).msg_id:
            raise AttributeError("This is the wrong message class for the given payload. Expected {}, got {}.".format(
                type(self).msg_id,
                payload[0]
            ))

        if len(payload) != 12:
            raise AttributeError("Payload length should be 12.")

        self.payload = payload
        self.values = [
            fields.PositionPinningField(payload[1]),
            fields.PinningSpeedField(payload[2:4]),
            fields.PinningCountField(payload[4:6]),
            fields.UnpinningSpeedField(payload[6:8]),
            fields.UnpinningCountField(payload[8:10]),
            fields.UnpinningDistanceField(payload[10:12]),
        ]

    def __str__(self):
        return """GPS position pinning is {}.
  {}: {}
  {}: {}
  {}: {}
  {}: {}
  {}: {}""".format(
            'on' if self.values[0].value else 'off',
            self.values[1].name, self.values[1],
            self.values[2].name, self.values[2],
            self.values[3].name, self.values[3],
            self.values[4].name, self.values[4],
            self.values[5].name, self.values[5],
        )


class GpsNavigationModeMessage(OutputMessage):
    msg_id = 0xb5
    name = 'TODO'
    description = '''

'''

    # noinspection PyMissingConstructor
    def __init__(self, payload):
        # Don't call super init.

        if payload[0] != type(self).msg_id:
            raise AttributeError("This is the wrong message class for the given payload. Expected {}, got {}.".format(
                type(self).msg_id,
                payload[0]
            ))

        # if len(payload) != :
        #     raise AttributeError("Payload length should be .")

        self.payload = payload
        # self.values = [
        #
        # ]

    def __str__(self):
        return "TODO"
        # return "{}".format(self.values)


class GpsPpsModeMessage(OutputMessage):
    msg_id = 0xb6
    name = 'TODO'
    description = '''

'''

    # noinspection PyMissingConstructor
    def __init__(self, payload):
        # Don't call super init.

        if payload[0] != type(self).msg_id:
            raise AttributeError("This is the wrong message class for the given payload. Expected {}, got {}.".format(
                type(self).msg_id,
                payload[0]
            ))

        # if len(payload) != :
        #     raise AttributeError("Payload length should be .")

        self.payload = payload
        # self.values = [
        #
        # ]

    def __str__(self):
        return "TODO"
        # return "{}".format(self.values)


output_message_types = {
    0x80: SoftwareVersionMessage,
    0x81: SoftwareCrcMessage,
    0x83: AckMessage,
    0x84: NackMessage,
    0x86: PositionUpdateRateMessage,
    0xae: GpsDatumMessage,
    0xb3: GpsWaasStatusMessage,
    0xb4: GpsPositionPinningStatusMessage,
    0xb5: GpsNavigationModeMessage,
    0xb6: GpsPpsModeMessage,
}
