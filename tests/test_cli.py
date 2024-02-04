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
