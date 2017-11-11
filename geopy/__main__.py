#!/user/bin/env python
from __future__ import print_function
import sys
from math import ceil
import argparse
from . import geocoders
from .exc import GeopyError
from .util import __version__

services = sorted(list(geocoders.SERVICE_TO_GEOCODER.keys()))
# formatting the long list of geocoders is a bit tricky
description = (
    'geopy is a client for several popular geocoding web services.'
    '\n\ngeocoders:\n\t' + '\n\t'.join([' '.join(services[i*5:i*5+5]) for i in range(ceil(len(services)/5))])
)
epilog = 'Copyright (c) 2006-2016 geopy authors'
usage = 'python -m geopy GEOCODER [address] [address ...]'


def main():
    parser = argparse.ArgumentParser(description=description, epilog=epilog, usage=usage, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--version', action='version', version='geopy ' + __version__)
    parser.add_argument('geocoder', metavar='geocoder', choices=services, help='One of the above geocoders')
    parser.add_argument('addresses', nargs='+', help='One or more addresses to geocode. Addresses must be surrounded by quotes')
    parser.add_argument('-c', '--credentials', metavar='key=value', action='append', help=(
        'Arguments to pass when the geocoder is instantiated.'
        ' e.g. api_key=<key>. '
        'May be repeated'
    ))

    args = parser.parse_args()

    # Convert key=value to {key: value}
    kwargs = {}
    if args.credentials:
        kwargs = dict(x.split('=') for x in args.credentials)

    geocoder = geocoders.get_geocoder_for_service(args.geocoder)(**kwargs)

    try:
        for address in args.addresses:
            location = geocoder.geocode(address)
            print('{}\t{}'.format(location.latitude, location.longitude))

    except GeopyError as e:
        print(e, file=sys.stderr)

if __name__ == '__main__':
    main()
