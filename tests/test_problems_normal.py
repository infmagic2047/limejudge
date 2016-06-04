from limejudge.problems import normal as problem_normal

from limejudge.judge import ResourceLimit


def test_from_dict():
    problem_data = {
        'name': 'foo',
        'input-file': 'foo.in',
        'output-file': 'foo.out',
        'source-path': 'foo/bar/baz',
        'testcases': [
            {
                'input-file': 'foo0.in',
                'output-file': 'foo0.out',
                'resource-limits': {
                    'time-limit': 1.5,
                    'memory-limit': 67108864,
                },
                'full-score': 10,
            },
            {
                'input-file': 'foo1.in',
                'output-file': 'foo1.out',
                'resource-limits': {
                    'time-limit': 2.5,
                    'memory-limit': 33554432,
                },
                'full-score': 20,
            },
        ],
    }
    problem = problem_normal.NormalProblem.from_dict(problem_data)

    assert problem.name == 'foo'
    assert problem.infile == 'foo.in'
    assert problem.outfile == 'foo.out'
    assert problem.progpath == 'foo/bar/baz'
    assert problem.testcases[0].infile == 'foo0.in'
    assert problem.testcases[0].outfile == 'foo0.out'
    assert (problem.testcases[0].rlimit ==
            ResourceLimit.from_dict(
                problem_data['testcases'][0]['resource-limits']))
    assert problem.testcases[0].full_score == 10
    assert problem.testcases[1].infile == 'foo1.in'
    assert problem.testcases[1].outfile == 'foo1.out'
    assert (problem.testcases[1].rlimit ==
            ResourceLimit.from_dict(
                problem_data['testcases'][1]['resource-limits']))
    assert problem.testcases[1].full_score == 20

    # Optional items
    assert problem.compiler_flags == {}
    assert problem.comp_method == 'no-extra-ws'

    problem_data['compiler-flags'] = {
        'c': '-O2 -lm',
        'cpp': '-O2',
    }
    problem_data['comparison-method'] = 'spj:foobar'
    problem2 = problem_normal.NormalProblem.from_dict(problem_data)

    assert problem2.compiler_flags == problem_data['compiler-flags']
    assert problem2.comp_method == 'spj:foobar'
