"""Simple judge tool for OI contests.

Usage:
    limejudge <command> [<args>...]
    limejudge --help
    limejudge --version

Available commands:
    autocreate    Create a contest configuration file automatically.
    resourcetest  Test the time and memory a program uses.
    runjudge      Judge the contest.

Options:
    -h, --help  Print this help message and exit.
    --version   Print version information and exit.
"""

import sys

from docopt import docopt

from limejudge import __version__
from limejudge.commands import UnknownCommandError, run_command_by_name


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = docopt(__doc__, argv=argv,
                  version='limejudge ' + __version__,
                  options_first=True)
    cmd_argv = [args['<command>']] + args['<args>']
    try:
        return run_command_by_name(args['<command>'], cmd_argv)
    except UnknownCommandError as err:
        print(str(err), file=sys.stderr)
        return 1
