import triade.cli as cli
from tests.helpers import CustomIO, custom_stdout


USAGE = cli.__doc__
VERSION = "0.3.0"
SUCCESS = 0
NO_VERSION = 3


class TestCLIScript:
    """Test the package's entrypoint script"""

    def test_triade_h(self):
        """test_script triade -h ::
        print usage information when calling script with -h flag"""
        with custom_stdout(["triade", "-h"]) as stream:
            status = cli.main()

        assert status == SUCCESS
        assert stream.read() == USAGE

    def test_triade_help(self):
        """test_script triade -h ::
        print usage information when calling script with --help flag"""
        with custom_stdout(["triade", "--help"]) as stream:
            status = cli.main()

        assert status == SUCCESS
        assert stream.read() == USAGE

    def test_triade_v(self):
        """test_script triade -v ::
        print version number when calling script with -v flag"""
        cli.__version__ = "0.3.0"
        with custom_stdout(["triade", "-v"]) as stream:
            status = cli.main()

        assert status == SUCCESS
        assert stream.read() == "%s\n" % (VERSION)

    def test_triade_version(self):
        """test_script triade -v ::
        print version number when calling script with --version flag"""
        cli.__version__ = "0.3.0"
        with custom_stdout(["triade", "--version"]) as stream:
            status = cli.main()

        assert status == SUCCESS
        assert stream.read() == "%s\n" % (VERSION)

    def test_triade_I_xml_O_yaml(self):
        """test_script triade -I xml -O yaml ::
        take an XML document from stdin and print it as YAML"""
        with open("tests/fixtures/test_xml/doc03.xml", "r") as file:
            input_data = file.read()

        expected_output = """childNodes:
- attributes:
    name: petroleum
  childNodes:
  - '78'
  tagName: commodity
- attributes:
    name: coffee
  childNodes:
  - '185'
  tagName: commodity
- attributes:
    name: gold
  childNodes:
  - '2023'
  tagName: commodity
- attributes:
    name: cocoa
  childNodes:
  - '4603'
  tagName: commodity
tagName: commodities
"""

        argv = ["triade", "-I", "xml", "-O", "yaml"]
        with CustomIO(argv, stdin=input_data, stdout=True) as result:
            status = cli.main()

        assert status == SUCCESS
        assert result.stdout == expected_output


class TestCLIFunctions:
    """Test the package's cli helper functions"""

    def test_show_help_function(self):
        """test_function show_help ::
        print usage information to stdout when calling show_help"""
        with custom_stdout() as stream:
            status = cli.show_help()

        assert status == SUCCESS
        assert stream.read() == USAGE

    def test_print_version_function(self):
        """test_function print_version ::
        print version number to stdout when calling print_version"""
        cli.__version__ = "0.3.0"
        with custom_stdout() as stream:
            status = cli.print_version()

        assert status == SUCCESS
        assert stream.read() == "%s\n" % (VERSION)

    def test_print_version_function_fail(self):
        """test_function print_version ::
        don't echo and return 3 when version number can't be retrieved"""
        cli.__version__ = None
        with custom_stdout() as stream:
            status = cli.print_version()

        assert status == NO_VERSION
        assert stream.read() == ""
