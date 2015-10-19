"""Judge the contest.

Usage:
    limejudge runjudge [options]
    limejudge runjudge --help

Options:
    -c, --contest=<file>         Use this contest configuration file.
                                 [default: contest.yaml]
    -p, --source-path=<path>     Only test this contestant. Contest
                                 results will not be written.
    -o, --output-results=<file>  Write contest results to this file.
                                 [default: results.yaml]
    -h, --help                   Print this help message and exit.
"""

import sys

import yaml
from docopt import docopt

from limejudge.contest import Contest
from limejudge.formatters.terminal import TerminalFormatter


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = docopt(__doc__, argv=argv)
    try:
        ct = Contest.from_yaml_file(args['--contest'])
    except FileNotFoundError:
        print('Contest configuration not found.', file=sys.stderr)
        return 1
    if args['--source-path'] is None:
        contest_results = ct.judge_all(TerminalFormatter())
        with open(args['--output-results'], 'w') as fout:
            fout.write(yaml.safe_dump(contest_results))
    else:
        ct.judge_contestant_path(args['--source-path'],
                                 TerminalFormatter())
