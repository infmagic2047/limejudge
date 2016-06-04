import os
import signal

from limejudge import judge


def test_resource_limit_from_dict():
    rlimit = judge.ResourceLimit.from_dict({'time-limit': 1.5,
                                            'memory-limit': 67108864})
    assert rlimit.time_limit == 1.5
    assert rlimit.memory_limit == 67108864


def test_resource_limit_equal():
    rlimit1 = judge.ResourceLimit.from_dict({'time-limit': 0.1,
                                             'memory-limit': 67108864})
    rlimit2 = judge.ResourceLimit.from_dict({'time-limit': 0.1,
                                             'memory-limit': 67108864})
    rlimit3 = judge.ResourceLimit.from_dict({'time-limit': 0.2,
                                             'memory-limit': 67108864})
    rlimit4 = judge.ResourceLimit.from_dict({'time-limit': 0.1,
                                             'memory-limit': 33554432})
    assert rlimit1 == rlimit2
    assert rlimit1 != rlimit3
    assert rlimit1 != rlimit4


def test_judge_run_time_limit_integer(tmpdir):
    testprog = os.path.join(os.path.dirname(__file__), 'progs',
                            'utime_limit.py')

    rlimit = judge.ResourceLimit(time_limit=1, memory_limit=256 << 20)
    jres, _ = judge.Judge([testprog, '0.95'], str(tmpdir), rlimit).run()
    assert jres == judge.JudgeResult.NORMAL

    rlimit = judge.ResourceLimit(time_limit=1, memory_limit=256 << 20)
    jres, _ = judge.Judge([testprog, '1.05'], str(tmpdir), rlimit).run()
    assert jres == judge.JudgeResult.TIME_LIMIT_EXCEEDED


def test_judge_run_time_limit_non_integer(tmpdir):
    testprog = os.path.join(os.path.dirname(__file__), 'progs',
                            'utime_limit.py')

    rlimit = judge.ResourceLimit(time_limit=0.5, memory_limit=256 << 20)
    jres, _ = judge.Judge([testprog, '0.45'], str(tmpdir), rlimit).run()
    assert jres == judge.JudgeResult.NORMAL

    rlimit = judge.ResourceLimit(time_limit=0.5, memory_limit=256 << 20)
    jres, _ = judge.Judge([testprog, '0.55'], str(tmpdir), rlimit).run()
    assert jres == judge.JudgeResult.TIME_LIMIT_EXCEEDED


def test_judge_run_time_limit_infinite_loop():
    testprog = os.path.join(os.path.dirname(__file__), 'progs',
                            'infinite_loop.py')

    rlimit = judge.ResourceLimit(time_limit=0.5, memory_limit=256 << 20)
    jres, _ = judge.Judge(testprog, None, rlimit).run()
    assert jres == judge.JudgeResult.TIME_LIMIT_EXCEEDED


def test_judge_run_time_usage(tmpdir):
    testprog = os.path.join(os.path.dirname(__file__), 'progs',
                            'utime_limit.py')

    rlimit = judge.ResourceLimit(time_limit=1, memory_limit=256 << 20)
    _, jru = judge.Judge([testprog, '0.5'], str(tmpdir), rlimit).run()
    with tmpdir.join('report').open() as fp:
        tuse = float(fp.read())
    assert abs(jru.time_usage - tuse) < 0.05


def test_judge_run_memory_limit(tmpdir):
    testprog = os.path.join(os.path.dirname(__file__), 'progs',
                            'memory_limit.py')

    rlimit = judge.ResourceLimit(time_limit=1, memory_limit=256 << 20)
    jres, _ = judge.Judge([testprog, '16'], str(tmpdir), rlimit).run()
    assert jres == judge.JudgeResult.NORMAL

    rlimit = judge.ResourceLimit(time_limit=1, memory_limit=256 << 20)
    jres, _ = judge.Judge([testprog, '256'], str(tmpdir), rlimit).run()
    assert jres == judge.JudgeResult.MEMORY_LIMIT_EXCEEDED


def test_judge_run_memory_usage(tmpdir):
    testprog = os.path.join(os.path.dirname(__file__), 'progs',
                            'memory_limit.py')

    rlimit = judge.ResourceLimit(time_limit=1, memory_limit=256 << 20)
    _, jru = judge.Judge([testprog, '16'], str(tmpdir), rlimit).run()
    with tmpdir.join('report').open() as fp:
        muse = float(fp.read())
    assert jru.memory_usage == muse


def test_judge_run_exit_status():
    testprog = os.path.join(os.path.dirname(__file__), 'progs',
                            'exit_status.py')

    rlimit = judge.ResourceLimit(time_limit=1, memory_limit=256 << 20)
    jres, _ = judge.Judge([testprog, '0'], None, rlimit).run()
    assert jres == judge.JudgeResult.NORMAL

    rlimit = judge.ResourceLimit(time_limit=1, memory_limit=256 << 20)
    jres, _ = judge.Judge([testprog, '1'], None, rlimit).run()
    assert jres == judge.JudgeResult.RUNTIME_ERROR


def test_judge_run_signal():
    testprog = os.path.join(os.path.dirname(__file__), 'progs',
                            'signal.py')

    rlimit = judge.ResourceLimit(time_limit=1, memory_limit=256 << 20)
    jres, _ = judge.Judge([testprog, str(int(signal.SIGSEGV))],
                          None, rlimit).run()
    assert jres == judge.JudgeResult.RUNTIME_ERROR

    rlimit = judge.ResourceLimit(time_limit=1, memory_limit=256 << 20)
    jres, _ = judge.Judge([testprog, str(int(signal.SIGKILL))],
                          None, rlimit).run()
    assert jres == judge.JudgeResult.RUNTIME_ERROR

    rlimit = judge.ResourceLimit(time_limit=1, memory_limit=256 << 20)
    jres, _ = judge.Judge([testprog, str(int(signal.SIGSTOP))],
                          None, rlimit).run()
    assert jres == judge.JudgeResult.RUNTIME_ERROR
