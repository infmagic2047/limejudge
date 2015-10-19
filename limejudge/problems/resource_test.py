"""Only test resource usage and ignore output file."""

import os
import shutil

from limejudge.judge import ResourceLimit
from limejudge.problems.runprog import RunProgramProblemBase


class _TestCase:
    def __init__(self, infile, rlimit):
        self.infile = infile
        self.rlimit = rlimit

    @property
    def full_score(self):
        return 1

    @classmethod
    def from_dict(cls, testcase_data):
        infile = testcase_data['input-file']
        rlimit_data = testcase_data['resource-limits']
        rlimit = ResourceLimit.from_dict(rlimit_data)
        return cls(infile, rlimit)


class ResourceTestProblem(RunProgramProblemBase):
    """A resource-testing problem."""

    def __init__(self, name, testcases, *, infile, progpath,
                 compiler_flags):
        RunProgramProblemBase.__init__(self, name, testcases)
        self.infile = infile
        self._progpath = progpath
        self._compiler_flags = compiler_flags

    @property
    def progpath(self):
        return self._progpath

    @property
    def compiler_flags(self):
        return self._compiler_flags

    def _judge_prepare_testcase(self, tmpdir, testcase):
        dst_in = os.path.join(tmpdir, self.infile)
        shutil.copyfile(testcase.infile, dst_in)

    def _judge_get_testcase_score(self, tmpdir, testcase):
        return testcase.full_score

    @classmethod
    def from_dict(cls, problem_data):
        name = problem_data['name']
        infile = problem_data['input-file']
        progpath = problem_data['source-path']
        testcases_data = problem_data['testcases']
        testcases = [_TestCase.from_dict(testcase_data)
                     for testcase_data in testcases_data]
        compiler_flags = problem_data.get('compiler-flags', {})
        return cls(name, infile=infile, progpath=progpath,
                   testcases=testcases, compiler_flags=compiler_flags)
