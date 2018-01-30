from common import byteorder
from messages import Message


class InputMessage(Message):
    """
    A Message from the host to the GPS unit.
    """

    def __str__(self):
        s = "GPS < Host: {}".format(type(self).name)
        for v in self.values:
            s += "\n  {}: {}".format(v.name, v)
        return s

    def get_payload(self):
        p = type(self).msg_id.to_bytes(1, byteorder=byteorder, signed=False)
        for v in self.values:
            p += bytes(v)
        return p


class SystemRestartMessage(InputMessage):
    msg_id = 0x01
    name = 'TODO'
    description = '''
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class QuerySoftwareVersionMessage(InputMessage):
    """

    >>> bytes(QuerySoftwareVersionMessage(software_type=0)).hex()
    'a0a100020200020d0a'

    >>> bytes(QuerySoftwareVersionMessage(software_type=1)).hex()
    'a0a100020201030d0a'

    """
    msg_id = 0x02
    name = 'Query software version'
    description = '''
This is a request message which is issued from the host to GPS receiver to retrieve loaded software version. The GPS
receiver should respond with an ACK along with information on software version when succeeded and should respond with an
NACK when failed. The payload length is 2 bytes.

Structure:
<0xA0,0xA1>< PL><02>< message body><CS><0x0D,0x0A>
'''

    def __init__(self, software_type):
        super().__init__()
        from fields import SoftwareTypeField
        self.values = [
            SoftwareTypeField(software_type)
        ]


class QuerySoftwareCrcMessage(InputMessage):
    msg_id = 0x03
    name = 'Query software CRC'
    description = '''
This is a request message which is issued from the host to GPS receiver to retrieve loaded software CRC. The GPS
receiver should respond with an ACK along with information on software version when succeeded and should respond with an
NACK when failed. The payload length is 2 bytes.

Structure:
<0xA0,0xA1>< PL><03>< message body><CS><0x0D,0x0A>
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class SetFactoryDefaultsMessage(InputMessage):
    msg_id = 0x04
    name = 'TODO'
    description = '''
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class ConfigureSerialPortMessage(InputMessage):
    """
    >>> bytes(ConfigureSerialPortMessage(rate=4800, permanent=False)).hex()
    'a0a1000405000000050d0a'
    """
    msg_id = 0x05
    name = 'Configure serial port'
    description = '''
This is a request message which will configure the serial COM port, baud rate. This command is issued from the
host to GPS receiver and GPS receiver should respond with an ACK or NACK. The payload length is 4 bytes.

Structure:
<0xA0,0xA1>< PL><05>< message body><CS><0x0D,0x0A>
'''

    def __init__(self, rate, permanent):
        super().__init__()
        from fields import ComPortField, BaudRateField, AttributesField
        self.values = [
            ComPortField(0),
            BaudRateField(BaudRateField.baud_rate_ids[rate]),
            AttributesField(permanent)
        ]


class ConfigureNmeaMessage(InputMessage):
    msg_id = 0x08
    name = 'TODO'
    description = '''
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class ConfigureOutputMessageFormatMessage(InputMessage):
    msg_id = 0x09
    name = 'TODO'
    description = '''
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class ConfigurePowerModeMessage(InputMessage):
    msg_id = 0x0C
    name = 'TODO'
    description = '''
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class ConfigurePositionUpdateRateMessage(InputMessage):
    """
    >>> bytes(ConfigurePositionUpdateRateMessage(1, False)).hex()
    'a0a100030e01000f0d0a'
    >>> print(ConfigurePositionUpdateRateMessage(20, True))
    GPS < Host: Configure position update rate
      Update rate: 20 Hz
      Attributes: update to both SRAM & FLASH
    """
    msg_id = 0x0E
    name = 'Configure position update rate'
    description = '''
This is a request message which is issued from the host to GPS receiver to configure the system position update rate.
Receivers with position rate 4 or higher needs to configure baud rate to 38400 or higher value.The GPS receiver should
respond with an ACK when succeeded and should respond with an NACK when failed. The payload length is 3 bytes.

Structure:
<0xA0,0xA1>< PL><0E>< message body><CS><0x0D,0x0A>
'''

    def __init__(self, rate, permanent):
        super().__init__()
        from fields import UpdateRateField, AttributesField
        self.values = [
            UpdateRateField(rate),
            AttributesField(permanent)
        ]


class QueryPositionUpdateRateMessage(InputMessage):
    msg_id = 0x10
    name = 'Query position update rate'
    description = '''
This is a request message which is issued from the host to GPS receiver to query position update rate. The GPS receiver
should respond with an ACK along with information on software version when succeeded and should respond with an NACK
when failed. The payload length is 1 byte.

Structure:
<0xA0,0xA1>< PL><10>< message body><CS><0x0D,0x0A>
'''

    def __init__(self):
        super().__init__()


class ConfigureDatumMessage(InputMessage):
    """

    >>> bytes(ConfigureDatumMessage(0x13, False)).hex()
    'a0a1001329001307ff7aff97fed9007ddf390046f41000ce0d0a'

    >>> print(ConfigureDatumMessage(0x00, True))
    GPS < Host: Configure datum
      Datum index: WGS-84 (0)
      Ellipsoid index: WGS 84 (23)
      Delta X: 0 m
      Delta Y: 0 m
      Delta Z: 0 m
      Semi-major axis: 6378137.0
      Inverse flattening: 298.2572236
      Attributes: update to both SRAM & FLASH
    """
    msg_id = 0x29
    name = 'Configure datum'
    description = '''
This is a request message which will setup parameters used for GPS position transformation. This command is issued from
the host to GPS receiver and GPS receiver should respond with an ACK or NACK. The payload length is 19 bytes.

Structure:
<0xA0,0xA1>< PL><29>< message body><CS><0x0D,0x0A>
'''

    def __init__(self, datum_index, permanent):
        super().__init__()

        from datums import datum_reference_list
        datum = datum_reference_list[datum_index]
        ellipsoid = datum.ellipsoid

        from fields import DatumIndexField, EllipsoidIndexField, DeltaXField, DeltaYField, DeltaZField, \
            SemiMajorAxisField, InverseFlatteningField, AttributesField
        self.values = [
            DatumIndexField(datum.index),
            EllipsoidIndexField(ellipsoid.index),
            DeltaXField(datum.delta_x),
            DeltaYField(datum.delta_y),
            DeltaZField(datum.delta_z),
            SemiMajorAxisField(ellipsoid.semi_major_axis),
            InverseFlatteningField(ellipsoid.inverse_flattening),
            AttributesField(permanent)
        ]


class QueryDatumMessage(InputMessage):
    msg_id = 0x2d
    name = 'Query datum'
    description = '''
This is a request message which is issued from the host to GPS receiver to retrieve used datum information. The GPS
receiver should respond with an ACK along with the datum information when succeeded and should respond with an NACK when
failed. The payload length is 1 byte.

Structure:
<0xA0,0xA1>< PL><2D>< message body><CS><0x0D,0x0A>
'''

    def __init__(self):
        super().__init__()


class GetEphemerisMessage(InputMessage):
    msg_id = 0x30
    name = 'TODO'
    description = '''
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class SetEphemerisMessage(InputMessage):
    msg_id = 0x31
    name = 'TODO'
    description = '''
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class ConfigureWaasMessage(InputMessage):
    msg_id = 0x37
    name = 'Query WAAS status'
    description = '''
This is a request message which is issued from the host to GPS receiver to query WAAS status. The GPS receiver should
respond with an ACK along with AGPS aiding status when succeeded and should respond with an NACK when failed. The
payload length is 1 byte.

Structure:
<0xA0,0xA1>< PL><38>< message body><CS><0x0D,0x0A>
'''

    def __init__(self):
        super().__init__()


class QueryWaasStatusMessage(InputMessage):
    msg_id = 0x38
    name = 'TODO'
    description = '''
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class ConfigurePositionPinningMessage(InputMessage):
    """

    >>> bytes(ConfigurePositionPinningMessage(True)).hex()
    'a0a100023901380d0a'

    >>> bytes(ConfigurePositionPinningMessage(False)).hex()
    'a0a100023900390d0a'

    """
    msg_id = 0x39
    name = 'Configure position pinning'
    description = '''
This is a request message which is issued from the host to GPS receiver to configure the system position pinning. The
GPS receiver should respond with an ACK when succeeded and should respond with an NACK when failed. The payload length
is 2 bytes.

Structure:
<0xA0,0xA1>< PL><39>< message body><CS><0x0D,0x0A>
'''

    def __init__(self, enable_position_pinning):
        super().__init__()
        from fields import PositionPinningField
        self.values = [
            PositionPinningField(enable_position_pinning)
        ]


class QueryPositionPinningMessage(InputMessage):
    """

    >>> bytes(QueryPositionPinningMessage()).hex()
    'a0a100013a3a0d0a'

    """
    msg_id = 0x3A
    name = 'Query position pinning'
    description = '''
This is a request message which is issued from the host to GPS receiver to query position pinning status. The GPS
receiver should respond with an ACK along with position pinning status when succeeded and should respond with an NACK
when failed. The payload length is 1 byte.

Structure:
<0xA0,0xA1>< PL><3A>< message body><CS><0x0D,0x0A>
'''

    def __init__(self):
        super().__init__()


class ConfigurePositionPinningParametersMessage(InputMessage):
    msg_id = 0x3B
    name = 'TODO'
    description = '''
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class ConfigureNavigationModeMessage(InputMessage):
    msg_id = 0x3C
    name = 'TODO'
    description = '''
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class QueryNavigationModeMessage(InputMessage):
    msg_id = 0x3D
    name = 'TODO'
    description = '''
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class ConfigurePpsModeMessage(InputMessage):
    msg_id = 0x3E
    name = 'TODO'
    description = '''
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class QueryPpsModeMessage(InputMessage):
    msg_id = 0x3F
    name = 'TODO'
    description = '''
'''

    def __init__(self):
        super().__init__()
        # from fields import
        # self.values = [
        #
        # ]


class UnknownMessage(InputMessage):
    msg_id = 0x00
    name = '?'


input_message_types = {
    0x00: UnknownMessage,
    0x01: SystemRestartMessage,
    0x02: QuerySoftwareVersionMessage,
    0x03: QuerySoftwareCrcMessage,
    0x04: SetFactoryDefaultsMessage,
    0x05: ConfigureSerialPortMessage,
    0x08: ConfigureNmeaMessage,
    0x0c: ConfigurePowerModeMessage,
    0x0e: ConfigurePositionUpdateRateMessage,
    0x10: QueryPositionUpdateRateMessage,
    0x29: ConfigureDatumMessage,
    0x2d: QueryDatumMessage,
    0x30: GetEphemerisMessage,
    0x31: SetEphemerisMessage,
    0x37: ConfigureWaasMessage,
    0x38: QueryWaasStatusMessage,
    0x39: ConfigurePositionPinningMessage,
    0x3a: QueryPositionPinningMessage,
    0x3b: ConfigurePositionPinningParametersMessage,
    0x3c: ConfigureNavigationModeMessage,
    0x3d: QueryNavigationModeMessage,
    0x3e: ConfigurePpsModeMessage,
    0x3f: QueryPpsModeMessage,
}
