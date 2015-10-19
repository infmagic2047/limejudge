#!/usr/bin/env python3

import sys


def main():
    if len(sys.argv) != 2:
        return 2
    return int(sys.argv[1])


if __name__ == '__main__':
    sys.exit(main())
