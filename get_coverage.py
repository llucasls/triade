import sys
import subprocess as sp
import os
import re
import time
from getopt import getopt


PYTEST = os.environ.get("PYTEST")


def print_chars(line, delay):
    for char in line:
        time.sleep(delay)
        sys.stdout.write(char)
        sys.stdout.flush()
    sys.stdout.write("\n")


def main():
    if PYTEST is None:
        msg = "Error: PYTEST environment variable is not defined"
        print(msg, file=sys.stderr)
        return 1

    use_color = sys.stdout.isatty()
    opts, _ = getopt(sys.argv[1:], "cC")
    for flag, _ in opts:
        if flag == "-c":
            use_color = True
        elif flag == "-C":
            use_color = False

    color = "--color=yes" if use_color else "--color=no"
    delay = 2E-04 if use_color else 3E-03

    proc = sp.run([PYTEST, "-q", "-s", "--cov=triade", color],
                  capture_output=True, text=True)

    lines = proc.stdout.strip().split("\n")

    fail_pat = re.compile(r"=+ FAILURES =+")
    cov_pat = re.compile(r"-+ coverage: .+ -+")
    tot_pat = re.compile(r"^TOTAL")

    fail_index = next((i for i, line in enumerate(lines) if fail_pat.match(line)), None)

    cov_index = next((i for i, line in enumerate(lines) if cov_pat.match(line)), None)

    total_index = next((i for i, line in enumerate(lines) if tot_pat.match(line)), None)

    # add cool factor to first line
    print_chars(lines[0], delay)
    if fail_index is not None:
        for line in lines[1:fail_index]:
            print(line)

        for line in lines[(cov_index - 1):(total_index + 1)]:
            print(line)

        print("\n", lines[-1], sep="")
    else:
        for line in lines[1:]:
            print(line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
