"""Core judge module."""

import os
import resource
import signal
import subprocess
from collections import namedtuple
from enum import Enum

from limejudge import ptrace


class JudgeResult(Enum):
    NORMAL = 0
    RUNTIME_ERROR = 1
    TIME_LIMIT_EXCEEDED = 2
    MEMORY_LIMIT_EXCEEDED = 3


_ResourceUsageBase = namedtuple('_ResourceUsageBase',
                                ['time_usage', 'memory_usage'])


class ResourceUsage(_ResourceUsageBase):
    def __new__(cls, *, time_usage, memory_usage):
        return _ResourceUsageBase.__new__(cls, time_usage, memory_usage)


class ResourceLimit:
    def __init__(self, *, time_limit, memory_limit):
        self.time_limit = time_limit
        self.memory_limit = memory_limit

    def __eq__(self, other):
        return (self.time_limit == other.time_limit and
                self.memory_limit == other.memory_limit)

    @classmethod
    def from_dict(cls, rlimit_data):
        time_limit = rlimit_data['time-limit']
        memory_limit = rlimit_data['memory-limit']
        return cls(time_limit=time_limit, memory_limit=memory_limit)


class Judge:
    """A Judge.

    It runs a command with resource limits and return the result.
    """

    def __init__(self, prog, cwd, limits):
        self.prog = prog
        self.cwd = cwd
        self.limits = limits

    def preexec(self):
        limit_cputime = int(self.limits.time_limit + 1.1)
        resource.setrlimit(resource.RLIMIT_CPU,
                           (limit_cputime, limit_cputime + 1))
        ptrace.traceme()

    def run(self):
        proc = subprocess.Popen(self.prog,
                                stderr=subprocess.DEVNULL,
                                preexec_fn=self.preexec,
                                cwd=self.cwd)

        tused = 0
        mused = 0

        while True:
            _, status, rusage = os.wait4(proc.pid, 0)
            tused = rusage.ru_utime

            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                if os.WIFEXITED(status) and not os.WEXITSTATUS(status):
                    result = JudgeResult.NORMAL
                else:
                    result = JudgeResult.RUNTIME_ERROR
                break

            # WIFSTOPPED
            if os.WSTOPSIG(status) == signal.SIGXCPU:
                proc.kill()
                result = JudgeResult.TIME_LIMIT_EXCEEDED
                break
            if os.WSTOPSIG(status) not in (signal.SIGTRAP,
                                           signal.SIGWINCH):
                proc.kill()
                result = JudgeResult.RUNTIME_ERROR
                break

            # Check time usage
            if tused > self.limits.time_limit:
                proc.kill()
                result = JudgeResult.TIME_LIMIT_EXCEEDED
                break

            # Check memory usage
            with open('/proc/{}/status'.format(proc.pid), 'r') as fp:
                for line in fp:
                    if line.startswith('VmPeak:'):
                        mused = int(line[7:-3]) * 1024
            if mused > self.limits.memory_limit:
                proc.kill()
                result = JudgeResult.MEMORY_LIMIT_EXCEEDED
                break

            try:
                ptrace.syscall(proc.pid, 0)
            except ProcessLookupError:
                # Child process dies
                pass

        resource_usage = ResourceUsage(time_usage=tused,
                                       memory_usage=mused)
        return result, resource_usage
