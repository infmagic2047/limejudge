"""Create a contest configuration file automatically.

Usage:
    limejudge autocreate [options]
    limejudge autocreate --help

Options:
    -c, --contest=<file>  Write contest configuration to this file.
                          [default: contest.yaml]
    -f, --force           Force writing contest configuration even if
                          the file already exists.
    --cflags=<flags>      Use extra C compiler flags for this contest.
    --cxxflags=<flags>    Use extra C++ compiler flags for this contest.
    -h, --help            Print this help message and exit.
"""

import os
import sys
from glob import glob

import yaml
from docopt import docopt


def ask_resource_limits(probname):
    time_limit = input(
        'What is the time limit (in s) for "' + probname + '"? ')
    time_limit = float(time_limit)
    if int(time_limit) == time_limit:
        time_limit = int(time_limit)
    memory_limit = input(
        'What is the memory limit (in MB) for "' + probname + '"? ')
    memory_limit = int(memory_limit) * 1024 * 1024
    return {
        'time-limit': time_limit,
        'memory-limit': memory_limit,
    }


def find_contestants(basedir):
    source_dir = os.path.join(basedir, 'source')
    contestants = []
    for name in sorted(os.listdir(source_dir)):
        if os.path.isdir(os.path.join(source_dir, name)):
            contestants.append({
                'name': name,
                'path': os.path.join('source', name),
            })
    return contestants


def find_testcases(basedir, probname):
    resource_limits = ask_resource_limits(probname)
    prob_dir = os.path.join(basedir, 'data', probname)
    has_in = {os.path.splitext(os.path.basename(x))[0]
              for x in glob(os.path.join(prob_dir, '*.in'))
              if os.path.isfile(x)}
    has_out = {os.path.splitext(os.path.basename(x))[0]
               for x in glob(os.path.join(prob_dir, '*.out'))
               if os.path.isfile(x)}
    testcases = []
    prob_reldir = os.path.join('data', probname)
    for testdata in sorted(has_in & has_out):
        testcases.append({
            'input-file': os.path.join(prob_reldir, testdata + '.in'),
            'output-file': os.path.join(prob_reldir, testdata + '.out'),
            'resource-limits': resource_limits,
        })
    if not testcases:
        return []
    testcase_cnt = len(testcases)
    full_score_each = 100 // testcase_cnt
    for testcase in testcases:
        testcase['full-score'] = full_score_each
    return testcases


def find_problems(basedir):
    data_dir = os.path.join(basedir, 'data')
    problems = []
    for name in sorted(os.listdir(data_dir)):
        if os.path.isdir(os.path.join(data_dir, name)):
            testcases = find_testcases(basedir, name)
            problems.append({
                'type': 'normal',
                'name': name,
                'input-file': name + '.in',
                'output-file': name + '.out',
                'source-path': name,
                'testcases': testcases,
            })
    return problems


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = docopt(__doc__, argv=argv)
    if os.path.exists(args['--contest']):
        if os.path.isdir(args['--contest']):
            print('Not overwriting directory.', file=sys.stderr)
            return 1
        elif not args['--force']:
            print('Not overwriting existing file.', file=sys.stderr)
            return 1
    cwd = os.getcwd()
    contest_data = {
        'metadata': {'title': os.path.basename(cwd)},
        'contestants': find_contestants(cwd),
        'problems': find_problems(cwd),
    }
    compiler_flags = {}
    if args['--cflags'] is not None:
        compiler_flags['c'] = args['--cflags'].strip()
    if args['--cxxflags'] is not None:
        compiler_flags['cpp'] = args['--cxxflags'].strip()
    if compiler_flags:
        for problem in contest_data['problems']:
            problem['compiler-flags'] = compiler_flags
    with open(args['--contest'], 'w') as fout:
        fout.write(yaml.safe_dump(contest_data))
