"""Contains various problem types."""


def create_problem_from_dict(problem_data):
    if problem_data['type'] == 'normal':
        from limejudge.problems.normal import NormalProblem as Problem
    elif problem_data['type'] == 'ansonly':
        from limejudge.problems.ansonly import AnsOnlyProblem as Problem
    elif problem_data['type'] == 'resource-test':
        from limejudge.problems.resource_test import (
            ResourceTestProblem as Problem)
    else:
        raise ValueError('Unknown problem type: ' +
                         repr(problem_data['type']))
    return Problem.from_dict(problem_data)
