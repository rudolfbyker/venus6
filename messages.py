from common import byteorder


class Message:

    msg_id = 0
    name = ''

    def __init__(self):
        self.values = []

    def get_payload(self):
        return b''

    def calculate_checksum(self):
        cs = 0
        for b in self.get_payload():
            cs ^= b
        return cs.to_bytes(1, byteorder=byteorder, signed=False)

    def __bytes__(self):
        payload = self.get_payload()
        return b'\xa0\xa1' + \
               len(payload).to_bytes(2, byteorder=byteorder, signed=False) + \
               payload + \
               self.calculate_checksum() + \
               b'\x0d\x0a'


class NmeaMessage:

    def __init__(self, nmea_string):
        self.nmea_string = nmea_string

    def __str__(self):
        return str(self.nmea_string)
