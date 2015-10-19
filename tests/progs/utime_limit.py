#!/usr/bin/env python3

import sys
from resource import RUSAGE_SELF, getrusage


def main():
    if len(sys.argv) != 2:
        return 2
    tlimit = float(sys.argv[1])
    i = 0
    while True:
        i += 1
        if i % 10000 == 0 and getrusage(RUSAGE_SELF).ru_utime > tlimit:
            break
    with open('report', 'w') as fout:
        fout.write('{}\n'.format(getrusage(RUSAGE_SELF).ru_utime))


if __name__ == '__main__':
    sys.exit(main())
