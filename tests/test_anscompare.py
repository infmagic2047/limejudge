import functools
import os

import pytest

from limejudge import anscompare


def test_compare_no_extra_ws(tmpdir):
    outfile = tmpdir.join('outfile')
    ansfile = tmpdir.join('ansfile')
    outname = str(outfile)
    ansname = str(ansfile)
    nonexistent = os.path.join(str(tmpdir), 'nonexistent')

    cmp_noextraws = functools.partial(anscompare.compare, 'no-extra-ws')

    # Same content
    outfile.write('1234abcd\nefgh5678\n')
    ansfile.write('1234abcd\nefgh5678\n')
    assert cmp_noextraws(None, outname, ansname, 42) == 42
    assert cmp_noextraws('ignored', outname, ansname, 42) == 42

    # Different content
    outfile.write('1234abcd\nefgh5678\n')
    ansfile.write('1234abcd\nefgh5679\n')
    assert cmp_noextraws(None, outname, ansname, 42) == 0

    # Ignore trailing whitespace
    outfile.write('1234abcd  \t\r\nefgh')
    ansfile.write('1234abcd\nefgh\n\r\n')
    assert cmp_noextraws(None, outname, ansname, 42) == 42

    # Don't ignore leading whitespace
    outfile.write(' 1234abcd\n')
    ansfile.write('1234abcd\n')
    assert cmp_noextraws(None, outname, ansname, 42) == 0

    # Non-existent files
    assert cmp_noextraws(None, nonexistent, ansname, 42) == 0
    assert cmp_noextraws(None, outname, nonexistent, 42) == 0
    assert cmp_noextraws(None, '', '', 42) == 0


def test_compare_spj(tmpdir):
    infile = tmpdir.join('infile')
    outfile = tmpdir.join('outfile')
    ansfile = tmpdir.join('ansfile')
    inname = str(infile)
    outname = str(outfile)
    ansname = str(ansfile)
    spjpath = os.path.join(os.path.dirname(__file__), 'progs', 'spj.py')
    relspjpath = os.path.relpath(spjpath)

    cmp_spj = functools.partial(anscompare.compare,
                                'special-judge:' + spjpath)
    cmp_relspj = functools.partial(anscompare.compare,
                                   'special-judge:' + relspjpath)

    # Call special judge with absolute or relative path
    infile.write('input')
    ansfile.write('answer')
    outfile.write('score 5')
    assert cmp_spj(inname, outname, ansname, 42) == 5
    assert cmp_relspj(inname, outname, ansname, 42) == 5

    # Input is checked correctly
    infile.write('bad-input')
    ansfile.write('answer')
    outfile.write('score 5')
    assert cmp_spj(inname, outname, ansname, 42) == 0

    # Answer is checked correctly
    infile.write('input')
    ansfile.write('bad-answer')
    outfile.write('score 5')
    assert cmp_spj(inname, outname, ansname, 42) == 0

    # Output is checked correctly
    infile.write('input')
    ansfile.write('answer')
    outfile.write('bad-score 5')
    assert cmp_spj(inname, outname, ansname, 42) == 0

    # Scores out of bound is returned as-is
    infile.write('input')
    ansfile.write('answer')
    outfile.write('score -1')
    assert cmp_spj(inname, outname, ansname, 42) == -1

    infile.write('input')
    ansfile.write('answer')
    outfile.write('score 43')
    assert cmp_spj(inname, outname, ansname, 42) == 43


def test_compare_invalid():
    with pytest.raises(ValueError) as err:
        anscompare.compare('invalid-comp-type', None, None, None, 0)
    assert 'Unknown comparison type:' in str(err)
