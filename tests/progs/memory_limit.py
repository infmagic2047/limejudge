#!/usr/bin/env python3

import sys


def main():
    if len(sys.argv) != 2:
        return 2
    mlimit = float(sys.argv[1])
    size = int(mlimit * 1024 * 1024)
    a = bytes(size)
    del a
    with open('/proc/self/status') as fp:
        for line in fp:
            if line.startswith('VmPeak:'):
                mused = int(line[7:-3]) * 1024
    with open('report', 'w') as fout:
        fout.write('{}\n'.format(mused))


if __name__ == '__main__':
    sys.exit(main())
