"""Answer-only problems."""

import os

from limejudge.anscompare import compare
from limejudge.problems.base import ProblemBase


class _TestCase:
    def __init__(self, infile, outfile, anspath, full_score):
        self.infile = infile
        self.outfile = outfile
        self.anspath = anspath
        self.full_score = full_score

    @classmethod
    def from_dict(cls, testcase_data):
        infile = testcase_data['input-file']
        outfile = testcase_data['output-file']
        anspath = testcase_data['answer-path']
        full_score = testcase_data['full-score']
        return cls(infile, outfile, anspath, full_score)


class AnsOnlyProblem(ProblemBase):
    """An answer-only problem."""

    def __init__(self, name, testcases, *, comp_method):
        ProblemBase.__init__(self, name, testcases)
        self.comp_method = comp_method

    def judge(self, src_path, formatter):
        formatter.problem_begin(self)
        tc_results = []
        for testcase in self.testcases:
            tc_result = self._judge_single_test(src_path, testcase,
                                                formatter)
            tc_results.append(tc_result)
        total_score = sum(result['score'] for result in tc_results)
        results = {
            'name': self.name,
            'testcases': tc_results,
            'total-score': total_score,
        }
        formatter.problem_end(self, results)
        return results

    def _judge_single_test(self, src_path, testcase, formatter):
        formatter.testcase_begin(testcase)
        ansfile = os.path.join(src_path, testcase.anspath)
        comp_result = compare(
            self.comp_method, testcase.infile, ansfile,
            testcase.outfile, testcase.full_score)
        result = {'score': comp_result}
        if comp_result >= testcase.full_score:
            result['verdict'] = 'Accepted'
        elif comp_result <= 0:
            result['verdict'] = 'Wrong answer'
        else:
            result['verdict'] = 'Partially accepted'
        formatter.testcase_end(testcase, result)
        return result

    @classmethod
    def from_dict(cls, problem_data):
        name = problem_data['name']
        testcases_data = problem_data['testcases']
        testcases = [_TestCase.from_dict(testcase_data)
                     for testcase_data in testcases_data]
        comp_method = problem_data.get('comparison-method',
                                       'no-extra-ws')
        return cls(name, testcases=testcases, comp_method=comp_method)
