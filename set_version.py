#!/usr/bin/env python

# Run this script with a '-h' or '--help' option to get usage and description.

usage = 'Usage:  %prog [options]'

description = '''
This script will sanitize json input while helping to set values.
'''

products = ['bronze', 'cloud', 'webstore']
environments = ['pre-prod', 'production', 'staging', 'staging-legacy','staging-firstwave',
    'cloud', 'firstwave', 'rad', 'radcloud', 'shop']

from optparse import OptionParser
import json
from datetime import datetime

def update_versions(infile, outfile, product, environment, version,
        comment):

    # Parse a json file to get a dictionary
    with open(infile, 'r') as filehandle:
        versions = json.load(filehandle)

    # Set specific values in the dictionary
    versions['products'][product]['environments'][environment]['version'] = \
        version
    versions['products'][product]['environments'][environment]['comment'] = \
        comment

    # Reoutput the json file
    with open(outfile, 'w') as filehandle:
        json.dump(versions, filehandle, sort_keys=True, indent=4,
            separators=(',', ': '))

if __name__ == '__main__':

    parser = OptionParser(usage=usage, description=description)

    parser.add_option('-i', '--infile', dest='infile',
        type='string', nargs=1, action='store', default='versions.json',
        help='JSON input file to process')

    parser.add_option('-o', '--outfile', dest='outfile',
        type='string', nargs=1, action='store', default='versions.json',
        help='JSON output file to process')

    parser.add_option('-p', '--product', dest='product',
        type='string', nargs=1, action='store',
        help='Product to be updated:  {}'.format(products))

    parser.add_option('-e', '--environment', dest='environment',
        type='string', nargs=1, action='store',
        help='Environment to be updated:  {}'.format(environments))

    parser.add_option('-v', '--version', dest='version',
        type='string', nargs=1, action='store',
        help='Name of the tag/commit/branch to enter')

    parser.add_option('-c', '--comment', dest='comment',
        type='string', nargs=1, action='store',
        help='Comment to try to describe the version')

    (options, args) = parser.parse_args()

    #parser.print_help()

    # Sanitize the product string
    if options.product not in products:
        parser.error('Product must be one of {}'.format(products))

    # Sanitize the environment string
    if options.environment not in environments:
        parser.error('Environment must be one of {}'.format(environments))

    # Produce a sensible UTC value to use for naming things
    tagtime = datetime.utcnow().strftime('%Y-%m-%d-%H%M')

    # Sanitize the version string
    if options.version is None or options.version == '':
        options.version = '{}-{}'.format(options.environment, tagtime)

    # Sanitize the comment string
    if options.comment is None:
        options.comment = '{} {} at {}'.format(options.product,
            options.environment, tagtime)

    # Fire off the version and comment string stuff
    update_versions(infile=options.infile, outfile=options.outfile,
        product=options.product, environment=options.environment,
        version=options.version, comment=options.comment)
