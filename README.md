versions
========

Version control for LightSpeed Cloud, Web Store, and Bronze

If you edit versions.json, validate it somehow please.

For example, it is possible to do it in the following way:

    ./set_version.py --product='cloud' --environment='staging' \
        --version='staging-2014-01-09-2030' \
        --comment='Squirrels made me do it'

or

    ./set_version.py -p 'cloud' -e 'staging' \
        -v 'staging-2014-01-09-2030' \
        -c 'Squirrels made me do it'

Additional help may be obtained by running it this way:

    ./set_version.py --help

or

    ./set_version.py -h
