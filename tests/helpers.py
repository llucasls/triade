import io
import sys
from contextlib import contextmanager


@contextmanager
def custom_stdout(argv=sys.argv):
    """Creates a new testing environment with an overriden standard output
    stream and a custom CLI arguments vector. This function is meant to be
    called in a context manager, where you can call the main function from
    an imported script and yields the new stdout stream, from where you can
    read a script's output.

    After closing, it will restore sys.argv and sys.stdout to their previous
    states."""
    old_argv = sys.argv
    old_stdout = sys.stdout
    sys.argv = argv
    sys.stdout = io.StringIO()
    try:
        yield sys.stdout
    finally:
        sys.stdout.seek(0)
        sys.argv = old_argv
        sys.stdout = old_stdout


class CustomIO:
    """Creates a new testing environment where you can optionally override the
    arguments vector and stdin, stdout and stderr streams. This class is meant
    to be instantiated in a context manager, from where you can call an
    imported script's main function using your custom parameters.

    The constructor takes a list of strings for argv, and defaults to the
    current sys.argv if it is not provided. For stdin, stdout and stderr, they
    each accept a boolean indicating if they are to be overriden, in which case
    a new StringIO will be made for each of them, or any buffer object that
    inherits from IOBase. The stdin argument also accepts a string, which will
    be written into a StringIO and used as input for the main function.

    After closing, each overriden stream will be restored to their previous
    state. You can still read the values from the resulting object outside the
    context manager."""
    def __init__(self, argv=sys.argv, *_, **streams):
        self._old_argv = sys.argv
        sys.argv = argv
        self._argv = argv

        self._override = {}

        if "stdin" in streams and streams["stdin"] is True:
            self._override["stdin"] = sys.stdin
            self._stdin = io.StringIO()
            sys.stdin = self._stdin
        elif "stdin" in streams and isinstance(streams["stdin"], str):
            self._override["stdin"] = sys.stdin
            self._stdin = io.StringIO()
            sys.stdin = self._stdin
            sys.stdin.write(streams["stdin"])
            sys.stdin.seek(0)
        elif "stdin" in streams and streams["stdin"]:
            if not isinstance(streams["stdin"], io.IOBase):
                raise TypeError("stdin should be a bool, str or IOBase object")

            self._override["stdin"] = sys.stdin
            self._stdin = streams["stdin"]
            sys.stdin = self._stdin

        if "stdout" in streams and streams["stdout"] is True:
            self._override["stdout"] = sys.stdout
            self._stdout = io.StringIO()
            sys.stdout = self._stdout
        elif "stdout" in streams and streams["stdout"]:
            if not isinstance(streams["stdout"], io.IOBase):
                raise TypeError("stdout should be a bool or IOBase object")

            self._override["stdout"] = sys.stdout
            self._stdout = streams["stdout"]
            sys.stdout = self._stdout

        if "stderr" in streams and streams["stderr"] is True:
            self._override["stderr"] = sys.stderr
            self._stderr = io.StringIO()
            sys.stderr = self._stderr
        elif "stderr" in streams and streams["stderr"]:
            if not isinstance(streams["stderr"], io.IOBase):
                raise TypeError("stderr should be a bool or IOBase object")

            self._override["stderr"] = sys.stderr
            self._stderr = streams["stderr"]
            sys.stderr = self._stderr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.argv = self._old_argv

        if "stdin" in self._override:
            sys.stdin = self._override["stdin"]

        if "stdout" in self._override:
            sys.stdout = self._override["stdout"]

        if "stderr" in self._override:
            sys.stderr = self._override["stderr"]

        return False

    @property
    def argv(self):
        """The argument vector passed to the test environment."""
        return self._argv

    @property
    def stdin(self):
        """The string passed to the testing environment as standard input.
        If sys.stdin was not overridden, it will return None."""
        try:
            return self._stdin.getvalue()
        except AttributeError:
            return None

    @property
    def stdout(self):
        """The resulting output message written to standard output.
        If sys.stdout was not overridden, it will return None."""
        try:
            return self._stdout.getvalue()
        except AttributeError:
            return None

    @property
    def stderr(self):
        """The resulting error message written to standard error.
        If sys.stderr was not overridden, it will return None."""
        try:
            return self._stderr.getvalue()
        except AttributeError:
            return None
