#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Run this script with a '-h' or '--help' option to get usage and description.


from optparse import OptionParser
import json
from datetime import datetime
import sys


usage = '''Usage:  %prog [options]'''

description = '''
This script will sanitize json input while helping to set values.
'''

products = [
    'bronze',
    'cloud',
    'pitcher',
    'reporting',
    'updater',
    'webclient',
    'webstore',
]
environments = [
    'cloud',
    'firstwave',
    'production',
    'rad',
    'radcloud',
    'shop',
    'staging',
    'staging-firstwave',
    'staging-legacy',
]


def update_versions(infile, outfile, product, environment, version, comment):
    '''Set specific JSON version paylod values'''

    versions = _get_json_from_file(infile)

    # Set specific values in the dictionary
    versions['products'][product]['environments'][environment]['version'] = \
        version
    versions['products'][product]['environments'][environment]['comment'] = \
        comment

    # Reoutput the json file
    with open(outfile, 'w') as filehandle:
        json.dump(versions, filehandle, sort_keys=True, indent=4,
                  separators=(',', ': '))


def _get_json_from_file(filename):
    '''Parse a json file to get a dictionary'''

    with open(filename, 'r') as filehandle:
        versions = json.load(filehandle)
    return versions


def get_version(infile, product, environment):
    '''Parse a json file to get a dictionary'''

    versions = _get_json_from_file(infile)

    return versions['products'][product]['environments'][environment]['version']


def parse_args(argv):
    '''Process command-line arguments'''

    parser = OptionParser(usage=usage, description=description)

    parser.add_option('-i', '--infile', dest='infile',
                      type='string', nargs=1, action='store',
                      default='versions.json',
                      help='(OPTIONAL) JSON input file to process')

    parser.add_option('-o', '--outfile', dest='outfile',
                      type='string', nargs=1, action='store',
                      default='versions.json',
                      help='(OPTIONAL) JSON output file to process')

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
                      help='(OPTIONAL) Comment to try to describe the version')

    parser.add_option('-g', '--get', dest='get',
                      type='int', nargs=1, action='store', default=0,
                      help='(OPTIONAL) set to 1 to get a console return of the value desired. Otherwise 0 assumed')

    (options, args) = parser.parse_args(argv)

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
        options.version = '{}-{}'.format(options.product, tagtime)

    # Sanitize the comment string
    if options.comment is None:
        options.comment = '{} {} at {}'.format(options.product,
                          options.environment, tagtime)

    return (options, args)


def do_work(options):
    '''Fire off the version and comment string stuff'''

    if options.get == 0:
        update_versions(infile=options.infile, outfile=options.outfile,
                        product=options.product,
                        environment=options.environment,
                        version=options.version, comment=options.comment)
    else:
        print get_version(infile=options.infile, product=options.product,
                          environment=options.environment)


def main(argv=None):
    '''main() flow.  Parse arguments and execute appropriate actions'''

    if argv is None:
        argv = sys.argv

    (options, args) = parse_args(argv)
    do_work(options)


if __name__ == '__main__':
    sys.exit(main())
