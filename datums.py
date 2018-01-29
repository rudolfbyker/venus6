
class Ellipsoid:

    def __init__(self, index, name, semi_major_axis, inverse_flattening):
        self.index = index
        self.name = name
        self.semi_major_axis = semi_major_axis
        self.inverse_flattening = inverse_flattening


class Datum:

    def __init__(self, index, name, delta_x, delta_y, delta_z, ellipsoid, region_of_use):
        self.index = index
        self.name = name
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_z = delta_z
        self.ellipsoid = ellipsoid
        self.region_of_use = region_of_use


ellipsoid_reference_list = {  # TODO fill in from appendix A in AN0003 (p44)
    7: Ellipsoid(7, 'Clarke 1880', 6378249.145, 293.465),
    23: Ellipsoid(23, 'WGS 84', 6378137, 298.257223563),
}

datum_reference_list = {  # TODO fill in from appendix B in AN0003 (p45ff)
    0: Datum(0, 'WGS-84', 0, 0, 0, ellipsoid_reference_list[23], 'Global'),
    19: Datum(19, 'Arc 1950', -134, -105, -295, ellipsoid_reference_list[7], 'Swaziland'),
    42: Datum(42, 'Cape', -136, -108, -292, ellipsoid_reference_list[7], 'South Africa'),
}


def convert(from_datum, to_datum, latitudes, longitudes):
    pass  # TODO!
