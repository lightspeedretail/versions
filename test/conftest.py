from ConfigParser import SafeConfigParser
import os
from UserDict import UserDict
import pytest
import shutil
from git import *

currentDir = os.path.dirname(os.path.abspath(__file__))
root_test_dir = os.path.dirname(currentDir) + '/test'
root_dir = os.path.dirname(root_test_dir)

safe_parser = SafeConfigParser()
abs_config_file = os.path.join(root_test_dir, "test_config.ini")
sample_config_file = os.path.join(root_test_dir, "test_config.ini.defaults")
safe_parser.read((sample_config_file, abs_config_file))


def pytest_configure(config):
    class WrappedDict(UserDict):

        def __getattr__(self, name):
            return self.data[name]

    for section in safe_parser.sections():
        wrapper = WrappedDict()
        setattr(config.option, section, wrapper)
        for key, value in safe_parser.items(section):
            wrapper.data[key] = unicode(value, 'utf8')


@pytest.fixture()
def clean_deploy_dir(request):
    workfldr = os.path.expandvars(request.config.option.General['workspace'])
    if os.path.exists(workfldr):
        shutil.rmtree(workfldr)


@pytest.fixture()
def verrepo(request):
    repo = Repo.clone_from(
        os.path.expandvars(request.config.option.General['repo']),
        os.path.expandvars(request.config.option.General['repoloc'])
    )
    return repo
