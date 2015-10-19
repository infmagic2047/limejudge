#!/usr/bin/env python3

import sys


def main():
    if len(sys.argv) != 5:
        return 2
    infile = sys.argv[1]
    outfile = sys.argv[2]
    ansfile = sys.argv[3]
    with open(infile) as fp:
        if fp.read() != 'input':
            return 1
    with open(ansfile) as fp:
        if fp.read() != 'answer':
            return 1
    with open(outfile) as fp:
        l = fp.read()
        if not l.startswith('score '):
            return 1
        print(l[6:])


if __name__ == '__main__':
    sys.exit(main())
