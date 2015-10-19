"""Test the time and memory a program uses.

Usage:
    limejudge resourcetest <time_limit> <memory_limit> <program>
                           <input_file>...
    limejudge resourcetest --help

Positional arguments:
    <time_limit>    Time limit in seconds.
    <memory_limit>  Memory limit in MB.
    <program>       Name of the program to test.
    <input_file>    Input file(s) to test with.

Options:
    -h, --help  Print this help message and exit.
"""

import sys

from docopt import docopt

from limejudge.contest import Contest
from limejudge.formatters.terminal import TerminalFormatter


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = docopt(__doc__, argv=argv)
    ct = Contest.from_dict({
        'metadata': {'title': 'Resource test'},
        'contestants': [{
            'name': 'Test',
            'path': '.',
        }],
        'problems': [{
            'type': 'resource-test',
            'name': 'Resource test',
            'input-file': args['<program>'] + '.in',
            'source-path': args['<program>'],
            'testcases': [
                {
                    'input-file': input_file,
                    'resource-limits': {
                        'time-limit': float(args['<time_limit>']),
                        'memory-limit':
                            int(float(args['<memory_limit>']) *
                                1024 * 1024),
                    },
                }
                for input_file in args['<input_file>']
            ],
        }],
    })
    ct.judge_all(TerminalFormatter())
