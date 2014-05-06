#!/usr/bin/env python

# Use this script to quickly locate tags

import argparse,os,json

parser=argparse.ArgumentParser(description="find current tag for product/environment",argument_default=None)
parser.add_argument('--product','-p',
    dest='product',
)
parser.add_argument('--environment','-e',
    dest='environment',
)
parser.add_argument('--version','-v',
    dest='version',
)

vfile=open('versions.json')

versions=json.load(vfile)
versions = versions['products']

def printformat(p,e,v):
    print "Product \"%s\" Environment \"%s\" has version \"%s\"" %(p,e,v)

args=parser.parse_args()
parsed_versions = {}

if args.product is not None and args.product in versions:
    parsed_versions[args.product] = {}
else: 
    for p in versions:
        parsed_versions[p] = {}

for p in parsed_versions:
    if args.environment is not None and args.environment in versions[p]['environments']:
        parsed_versions[p][args.environment] = {}
    elif args.environment is None:
        for e in versions[p]['environments']:
            parsed_versions[p][e] = {}

    for e in parsed_versions[p]:
        if args.version is not None and args.version == versions[p]['environments'][e]['version']:
            parsed_versions[p][e] = versions[p]['envoronments'][e]['version']
        elif args.version is None:
            parsed_versions[p][e] = versions[p]['environments'][e]['version']

for p in parsed_versions:
    print "Product: %s" %p
    if len(parsed_versions[p]) == 0:
        print "  None"
    for e in parsed_versions[p]:
        print "  %s: %s" %(e, parsed_versions[p][e])
vfile.close()
