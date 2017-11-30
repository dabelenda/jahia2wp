import pytest
import yaml
import os
from importlib import reload
import settings
from wordpress import WPPluginList

SITE_URL_GENERIC = "http://localhost/"
SITE_URL_SPECIFIC = "http://localhost/{}".format(settings.TEST_SITE)
os.environ["PLUGINS_CONFIG_BASE_PATH"] = "wordpress/tests/plugins"
reload(settings)

"""
If you want to execute pytest locally to your computer (= not on Travis), you have to :
$ make exec
$ vjahia
$ pytest -x wordpress/tests/test_plugins.py
"""


@pytest.fixture(scope="module")
def wp_plugin_list():
    return WPPluginList(
        settings.PLUGINS_CONFIG_GENERIC_FOLDER,
        'config-lot1.yml',
        settings.PLUGINS_CONFIG_SPECIFIC_FOLDER)


def test_yaml_include():
    # Generate filename to open regarding current script path
    yaml_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'yaml-root.yml')
    yaml_content = yaml.load(open(yaml_path, 'r'))
    assert yaml_content['root_value'] == 'root'
    assert yaml_content['included_value'] == 'included'


class TestWPPluginList:

    def test_generic_plugin_list(self, wp_plugin_list):
        plugins_to_test = ['add-to-any', 'hello', 'akismet']

        plugin_list = wp_plugin_list.plugins()
        assert len(plugin_list) == len(plugins_to_test)
        for plugin_name in plugins_to_test:
            assert plugin_name in plugin_list

    def test_specific_plugin_list(self, wp_plugin_list):
        plugins_to_test = ['add-to-any', 'hello', 'redirection', 'akismet']

        plugin_list = wp_plugin_list.plugins(settings.TEST_SITE)
        assert len(plugin_list) == len(plugins_to_test)
        for plugin_name in plugins_to_test:
            assert plugin_name in plugin_list
