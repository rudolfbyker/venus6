from common import byteorder
from datums import ellipsoid_reference_list, datum_reference_list


class Field:
    pass


class Uint8Field(Field):
    """
    >>> str(Uint8Field(5))
    '0x05'
    """
    n_bytes = 1
    allowed_values = None

    def __init__(self, value):
        super().__init__()

        if type(value) is bytes:
            value = int.from_bytes(bytes=value, byteorder=byteorder, signed=False)

        if type(value) is bool:
            value = int(value)

        if type(value) is not int:
            raise AttributeError("Value must be an integer, or bytes that can be interpreted as an integer.")

        if type(self).allowed_values is not None and value not in type(self).allowed_values:
            raise AttributeError("Value {} not allowed. Allowed values are: {}".format(
                value,
                type(self).allowed_values.keys()
            ))
        if value >= 256:
            raise AttributeError("Value must be under 256. Got {}.".format(value))
        if value < 0:
            raise AttributeError("Value must be positive. Got {}.".format(value))

        self.value = value

    def __bytes__(self):
        return int(self.value).to_bytes(1, byteorder=byteorder, signed=False)

    def __str__(self):
        return "0x{:02x}".format(int(self.value))


class Uint16Field(Field):
    """
    >>> str(Uint16Field(5))
    '0x0005'
    >>> Uint16Field(b'\\x0F\\x00').value
    3840
    """
    n_bytes = 2
    allowed_values = None

    def __init__(self, value):
        super().__init__()

        if type(value) is bytes:
            value = int.from_bytes(bytes=value, byteorder=byteorder, signed=False)

        if type(value) is bool:
            value = int(value)

        if type(value) is not int:
            raise AttributeError("Value must be an integer, or bytes that can be interpreted as an integer.")

        if type(self).allowed_values is not None and value not in type(self).allowed_values:
            raise AttributeError("Value {} not allowed. Allowed values are: {}".format(
                value,
                type(self).allowed_values.keys()
            ))
        if value >= 65536:
            raise AttributeError("Value must be under 65536. Got {}.".format(value))
        if value < 0:
            raise AttributeError("Value must be positive. Got {}.".format(value))

        self.value = value

    def __bytes__(self):
        return int(self.value).to_bytes(2, byteorder=byteorder, signed=False)

    def __str__(self):
        return "0x{:04x}".format(int(self.value))


class Sint16Field(Field):
    """
    >>> str(Sint16Field(5))
    '0x0005'
    >>> Sint16Field(b'\\x0F\\x00').value
    3840
    """
    n_bytes = 2
    allowed_values = None

    def __init__(self, value):
        super().__init__()

        if type(value) is bytes:
            value = int.from_bytes(bytes=value, byteorder=byteorder, signed=False)

        if type(value) is bool:
            value = int(value)

        if type(value) is not int:
            raise AttributeError("Value must be an integer, or bytes that can be interpreted as an integer.")

        if type(self).allowed_values is not None and value not in type(self).allowed_values:
            raise AttributeError("Value {} not allowed. Allowed values are: {}".format(
                value,
                type(self).allowed_values.keys()
            ))
        if value >= 32768:
            raise AttributeError("Value must be under 32768. Got {}.".format(value))
        if value < -32768:
            raise AttributeError("Value must be above or equal to -32768. Got {}.".format(value))

        self.value = value

    def __bytes__(self):
        return int(self.value).to_bytes(2, byteorder=byteorder, signed=True)

    def __str__(self):
        return "0x{:04x}".format(int(self.value))


class Uint32Field(Field):
    """
    >>> str(Uint32Field(5))
    '0x00000005'
    """
    n_bytes = 4
    allowed_values = None

    def __init__(self, value):
        super().__init__()

        if type(value) is bytes:
            value = int.from_bytes(bytes=value, byteorder=byteorder, signed=False)

        if type(value) is bool:
            value = int(value)

        if type(value) is not int:
            raise AttributeError("Value must be an integer, or bytes that can be interpreted as an integer.")

        if type(self).allowed_values is not None and value not in type(self).allowed_values:
            raise AttributeError("Value {} not allowed. Allowed values are: {}".format(
                value,
                type(self).allowed_values.keys()
            ))
        if value >= 4294967296:
            raise AttributeError("Value must be under 4294967296. Got {}.".format(value))
        if value < 0:
            raise AttributeError("Value must be positive. Got {}.".format(value))

        self.value = value

    def __bytes__(self):
        return int(self.value).to_bytes(4, byteorder=byteorder, signed=False)

    def __str__(self):
        return "0x{:04x}".format(int(self.value))


class SoftwareTypeField(Uint8Field):
    allowed_values = {0: 'reserved', 1: 'system code'}
    name = 'Software Type'


class AckIdField(Uint8Field):
    from input_messages import input_message_types
    allowed_values = input_message_types
    name = 'ACK ID'


class KernelVersionField(Uint32Field):
    """
    >>> KernelVersionField(b'\\x00\\x00\\x00\\x11').value
    17
    >>> str(KernelVersionField(b'\\x00\\x00\\x00\\x11'))
    '0.0.17'
    >>> str(KernelVersionField(b'\\x00\\x01\\x00\\x01'))
    '1.0.1'
    """
    name = 'kernel version'
    description = 'X1.Y1.Z1 = SkyTraq Kernel Version Ex. X1=01, Y1=00, Z1=01 (1.0.1)'

    def __str__(self):
        return "{}.{}.{}".format(
            self.x(),
            self.y(),
            self.z()
        )

    def x(self):
        return (self.value & 0xFF0000) >> 16

    def y(self):
        return (self.value & 0xFF00) >> 8

    def z(self):
        return self.value & 0xFF


class OdmVersionField(Uint32Field):
    name = 'odm version'
    description = 'X1.Y1.Z1 = SkyTraq Version Ex. X1=01, Y1=03, Z1=01 (1.3.1)'

    def __str__(self):
        return "{}.{}.{}".format(
            self.x(),
            self.y(),
            self.z()
        )

    def x(self):
        return (self.value & 0xFF0000) >> 16

    def y(self):
        return (self.value & 0xFF00) >> 8

    def z(self):
        return self.value & 0xFF


class RevisionField(Uint32Field):
    """
    TODO: is the example in the application note wrong?
    >>> f = RevisionField(b'\\x00\\x06\\x0c\\x0f')
    >>> f.value
    396303
    >>> f.yy()
    6
    >>> f.mm()
    12
    >>> f.dd()
    15
    >>> str(f)
    '06-12-15'
    """
    name = 'revision'
    description = 'YYMMDD = SkyTraq Revision Ex. YY=06, MM=01, DD=10 (060110)'

    def __str__(self):
        return "{:02d}-{:02d}-{:02d}".format(
            self.yy(),
            self.mm(),
            self.dd()
        )

    def yy(self):
        return (self.value & 0xFF0000) >> 16

    def mm(self):
        return (self.value & 0xFF00) >> 8

    def dd(self):
        return self.value & 0xFF


class CrcField(Uint16Field):
    name = 'CRC'


class UpdateRateField(Uint8Field):
    name = 'Update rate'
    unit = 'Hz'
    allowed_values = [1, 2, 4, 5, 8, 10, 20]

    def __str__(self):
        return "{} {}".format(self.value, type(self).unit)


class WaasStatusField(Uint8Field):
    name = 'WAAS status'
    allowed_values = {0: 'disable', 1: 'enable'}


class PositionPinningField(Uint8Field):
    name = 'Position pinning'
    allowed_values = {0: 'disable', 1: 'enable'}


class PinningSpeedField(Uint16Field):
    name = 'Pinning speed'
    unit = 'km/h'

    def __str__(self):
        return "{} {}".format(self.value, type(self).unit)


class PinningCountField(Uint16Field):
    name = 'Pinning count'
    unit = 's'

    def __str__(self):
        return "{} {}".format(self.value, type(self).unit)


class UnpinningSpeedField(Uint16Field):
    name = 'Unpinning speed'
    unit = 'km/h'

    def __str__(self):
        return "{} {}".format(self.value, type(self).unit)


class UnpinningCountField(Uint16Field):
    name = 'Unpinning count'
    unit = 's'

    def __str__(self):
        return "{} {}".format(self.value, type(self).unit)


class UnpinningDistanceField(Uint16Field):
    name = 'Unpinning distance'
    unit = 'm'

    def __str__(self):
        return "{} {}".format(self.value, type(self).unit)


class EllipsoidIndexField(Uint8Field):
    name = 'Ellipsoid index'
    allowed_values = ellipsoid_reference_list

    def __str__(self):
        ellipsoid = ellipsoid_reference_list[self.value]
        return "{} ({})".format(
            ellipsoid.name,
            ellipsoid.index
        )


class DatumIndexField(Uint16Field):
    name = 'Datum index'
    allowed_values = datum_reference_list

    def __str__(self):
        datum = datum_reference_list[self.value]
        return "{} ({})".format(
            datum.name,
            datum.index
        )


class DeltaXField(Sint16Field):
    name = 'Delta X'
    unit = 'm'

    def __str__(self):
        return "{} {}".format(self.value, type(self).unit)


class DeltaYField(Sint16Field):
    name = 'Delta Y'
    unit = 'm'

    def __str__(self):
        return "{} {}".format(self.value, type(self).unit)


class DeltaZField(Sint16Field):
    name = 'Delta Z'
    unit = 'm'

    def __str__(self):
        return "{} {}".format(self.value, type(self).unit)


class SemiMajorAxisField(Uint32Field):
    """
    >>> SemiMajorAxisField(6378249.145).value
    8249145
    """
    name = 'Semi-major axis'

    def __init__(self, value):
        super().__init__(int(round((value - 6370000) * 1000)))

    # TODO: use the @property decorator?
    def getValue(self):
        return (self.value / 1000.) + 6370000

    def __str__(self):
        return "{}".format(self.getValue())


class InverseFlatteningField(Uint32Field):
    """
    >>> InverseFlatteningField(293.465).value
    4650000
    """
    name = 'Inverse flattening'

    def __init__(self, value):
        super().__init__(int(round((value - 293) * 10000000)))

    # TODO: use the @property decorator?
    def getValue(self):
        return (self.value / 10000000.) + 293

    def __str__(self):
        return "{}".format(self.getValue())


class AttributesField(Uint8Field):
    name = 'Attributes'
    allowed_values = {0: 'update to SRAM', 1: 'update to both SRAM & FLASH'}

    def __str__(self):
        return type(self).allowed_values[self.value]


class BaudRateField(Uint8Field):
    name = 'Baud rate'
    unit = 'bps'
    allowed_values = {
        0: 4800,
        1: 9600,
        2: 19200,
        3: 38400,
        4: 57600,
        5: 115200,
    }

    def __str__(self):
        return "{} {}".format(self.value, type(self).unit)


class ComPortField(Uint8Field):
    name = 'COM port'
    allowed_values = {0: 'COM1'}

    def __str__(self):
        return type(self).allowed_values[self.value]
