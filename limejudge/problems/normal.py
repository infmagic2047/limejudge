"""Normal problems with one input file and one output file."""

import os
import shutil

from limejudge.anscompare import compare
from limejudge.judge import ResourceLimit
from limejudge.problems.runprog import RunProgramProblemBase


class _TestCase:
    def __init__(self, infile, outfile, rlimit, full_score):
        self.infile = infile
        self.outfile = outfile
        self.rlimit = rlimit
        self.full_score = full_score

    @classmethod
    def from_dict(cls, testcase_data):
        infile = testcase_data['input-file']
        outfile = testcase_data['output-file']
        rlimit_data = testcase_data['resource-limits']
        rlimit = ResourceLimit.from_dict(rlimit_data)
        full_score = testcase_data['full-score']
        return cls(infile, outfile, rlimit, full_score)


class NormalProblem(RunProgramProblemBase):
    """A normal problem."""

    def __init__(self, name, testcases, *, infile, outfile, progpath,
                 compiler_flags, comp_method):
        RunProgramProblemBase.__init__(self, name, testcases)
        self.infile = infile
        self.outfile = outfile
        self._progpath = progpath
        self._compiler_flags = compiler_flags
        self.comp_method = comp_method

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
        dst_out = os.path.join(tmpdir, self.outfile)
        return compare(self.comp_method, testcase.infile, dst_out,
                       testcase.outfile, testcase.full_score)

    @classmethod
    def from_dict(cls, problem_data):
        name = problem_data['name']
        infile = problem_data['input-file']
        outfile = problem_data['output-file']
        progpath = problem_data['source-path']
        testcases_data = problem_data['testcases']
        testcases = [_TestCase.from_dict(testcase_data)
                     for testcase_data in testcases_data]
        compiler_flags = problem_data.get('compiler-flags', {})
        comp_method = problem_data.get('comparison-method',
                                       'no-extra-ws')
        return cls(name, infile=infile, outfile=outfile,
                   progpath=progpath, testcases=testcases,
                   compiler_flags=compiler_flags,
                   comp_method=comp_method)
