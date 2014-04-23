# -*- coding: utf-8 -*-
from set_version import update_versions, parse_args, do_work, get_version, _get_json_from_file
import pytest
import subprocess
import os


@pytest.mark.usefixtures("clean_deploy_dir")
class TestGeneral(object):
    def test_setversionset(self, verrepo):
        verfolder = verrepo.working_dir
        retr = subprocess.call([os.path.expandvars('$VERSION_PATH')+'/set_version.py',
                               '--product=webstore',
                               '--environment=staging',
                               '--version=' + 'taggy_tag',
                               '--comment=' + 'life is bad',
                               '--infile=' + verfolder + '/versions.json',
                               '--outfile=' + verfolder + '/versions.json'])
        assert retr == 0
        #make sure there is a changed file
        assert len(verrepo.head.commit.diff(None)) == 1

    def test_setversionget(self, verrepo):
        verfolder = verrepo.working_dir
        retr = subprocess.check_output([os.path.expandvars('$VERSION_PATH')+'/set_version.py',
                                        '--product=webstore',
                                        '--environment=staging',
                                        '--infile=' + verfolder + '/versions.json',
                                        '--get=1'], cwd=verfolder)
        assert 'webstore' in retr
        #make sure there is a changed file
        assert len(verrepo.head.commit.diff(None)) == 0

    def test_getversion(self, verrepo):
        verfolder = verrepo.working_dir
        ver = get_version(infile=verfolder + '/versions.json',
                          product='webstore',
                          environment='staging')
        assert len(verrepo.head.commit.diff(None)) == 0
        assert 'webstore' in ver  # crappy validation since the file changes

    def test_updateversions(self, verrepo):
        verfolder = verrepo.working_dir
        #infile, outfile, product, environment, version, comment
        update_versions(infile=verfolder + '/versions.json',
                        outfile=verfolder + '/versions.json',
                        product='webstore',
                        environment='staging',
                        version='thisismytag',
                        comment='this is my comment')

        # assert checking the file, blah.
        assert len(verrepo.head.commit.diff(None)) == 1

    def test_parseargsSet(self, longargset):
        (options, argv) = parse_args(longargset)
        assert options.product == 'webstore'
        assert options.environment == 'staging'
        assert options.version == 'taggy_tag'
        assert options.comment == 'life is bad'
        assert options.infile == 'versions.json'
        assert options.outfile == 'versions.json'
        assert options.get == 0

    def test_parseargshortSet(self, shortargset):
        (options, argv) = parse_args(shortargset)
        assert options.product == 'webstore'
        assert options.environment == 'staging'
        assert options.version == 'taggy_tag'
        assert options.comment == 'life is bad'
        assert options.infile == 'versions.json'
        assert options.outfile == 'versions.json'
        assert options.get == 0

    def test_doworkSet(self, optionsset, verrepo):
        verfolder = verrepo.working_dir
        verfilepath = verfolder + '/versions.json'
        optionsset.infile = verfilepath
        optionsset.outfile = verfilepath

        do_work(optionsset)
        assert len(verrepo.head.commit.diff(None)) == 1

    def test_parseargsGet(self, longargget):
        (options, argv) = parse_args(longargget)
        assert options.product == 'webstore'
        assert options.environment == 'staging'
        assert 'webstore' in options.version
        assert 'webstore' in options.comment
        assert options.infile == 'versions.json'
        assert options.outfile == 'versions.json'
        assert options.get == 1

    def test_doworkGet(self, optionsget, verrepo):
        verfolder = verrepo.working_dir
        verfilepath = verfolder + '/versions.json'
        optionsget.infile = verfilepath
        optionsget.outfile = verfilepath

        do_work(optionsget)
        assert len(verrepo.head.commit.diff(None)) == 0

    def test_versionopen(self):
        version = _get_json_from_file(os.path.expandvars('$VERSION_PATH') + '/versions.json')
        assert version is not None

    @pytest.fixture()
    def longargset(self):
        arguments = ['--product=webstore',
                     '--environment=staging',
                     '--version=taggy_tag',
                     '--comment=life is bad',
                     '--infile=versions.json',
                     '--outfile=versions.json']
        return arguments

    @pytest.fixture()
    def longargget(self):
        arguments = ['--product=webstore',
                     '--environment=staging',
                     '--infile=versions.json',
                     '--get=1']
        return arguments

    @pytest.fixture()
    def shortargset(self):
        arguments = ['-pwebstore',
                     '-estaging',
                     '-vtaggy_tag',
                     '-clife is bad',
                     '-iversions.json',
                     '-oversions.json']
        return arguments

    @pytest.fixture()
    def optionsset(self, longargset):
        (opts, argv) = parse_args(longargset)
        return opts

    @pytest.fixture()
    def optionsget(self, longargget):
        (opts, argv) = parse_args(longargget)
        return opts
