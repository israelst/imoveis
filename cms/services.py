import geocoder


def address_to_point(address):
    g = geocoder.osm(address)

    if not g.ok:
        raise ValueError('invalid address: "{}"'.format(address))

    return tuple(g.latlng)
