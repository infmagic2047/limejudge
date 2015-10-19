#!/usr/bin/env python3

import os
import sys


def main():
    if len(sys.argv) != 2:
        return 2
    os.kill(os.getpid(), int(sys.argv[1]))


if __name__ == '__main__':
    sys.exit(main())
