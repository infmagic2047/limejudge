"""Base of problems with a program to be tested."""

import os
from abc import abstractmethod
from tempfile import TemporaryDirectory

from limejudge import compiling
from limejudge.problems.base import ProblemBase
from limejudge.judge import Judge, JudgeResult


class RunProgramProblemBase(ProblemBase):
    """A problem tested by compiling and running a program."""

    @property
    @abstractmethod
    def progpath(self):
        """Path to the tested program, relative to source path."""

    @property
    @abstractmethod
    def compiler_flags(self):
        """Dict of flags for the compiler."""

    def judge(self, src_path, formatter):
        formatter.problem_begin(self)
        with TemporaryDirectory() as tmpdir:
            prog = os.path.join(tmpdir, os.path.basename(self.progpath))
            progsrc = os.path.join(src_path, self.progpath)
            try:
                compiling.compile_into(
                    progsrc, prog, compiler_flags=self.compiler_flags)
            except compiling.CompileError:
                formatter.problem_verdict(self, 'Compile error')
                results = {
                    'verdict': 'Compile error',
                    'total-score': 0,
                }
            except compiling.NoSourceFileError:
                formatter.problem_verdict(self,
                                          'Cannot find source file')
                results = {
                    'verdict': 'Cannot find source file',
                    'total-score': 0,
                }
            else:
                results = self._judge_tests(prog, formatter)
        results['name'] = self.name
        formatter.problem_end(self, results)
        return results

    def _judge_tests(self, prog, formatter):
        tc_results = []
        for testcase in self.testcases:
            tc_result = self._judge_single_test(prog, testcase,
                                                formatter)
            tc_results.append(tc_result)
        total_score = sum(result['score'] for result in tc_results)
        return {
            'testcases': tc_results,
            'total-score': total_score,
        }

    def _judge_single_test(self, prog, testcase, formatter):
        formatter.testcase_begin(testcase)
        with TemporaryDirectory() as tmpdir:
            self._judge_prepare_testcase(tmpdir, testcase)
            tj = Judge(prog, tmpdir, testcase.rlimit)
            tjres, tjru = tj.run()
            if tjres == JudgeResult.RUNTIME_ERROR:
                result = {
                    'verdict': 'Runtime error',
                    'score': 0,
                }
            elif tjres == JudgeResult.TIME_LIMIT_EXCEEDED:
                result = {
                    'verdict': 'Time limit exceeded',
                    'score': 0,
                }
            elif tjres == JudgeResult.MEMORY_LIMIT_EXCEEDED:
                result = {
                    'verdict': 'Memory limit exceeded',
                    'score': 0,
                }
            else:
                score = self._judge_get_testcase_score(tmpdir, testcase)
                time_usage = round(tjru.time_usage, 3)
                memory_usage = tjru.memory_usage
                result = {
                    'score': score,
                    'time-usage': time_usage,
                    'memory-usage': memory_usage,
                }
                if score >= testcase.full_score:
                    result['verdict'] = 'Accepted'
                elif score <= 0:
                    result['verdict'] = 'Wrong answer'
                else:
                    result['verdict'] = 'Partially accepted'
        formatter.testcase_end(testcase, result)
        return result

    @abstractmethod
    def _judge_prepare_testcase(self, tmpdir, testcase):
        """Prepare testcase for running in tmpdir."""

    @abstractmethod
    def _judge_get_testcase_score(self, tmpdir, testcase):
        """Get score of testcase which was run in tmpdir."""
