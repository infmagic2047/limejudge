"""Compare program output and provided answer."""

import subprocess


def compare(comp_type, infile, outfile, ansfile, full_score):
    """Compare answers using comparison type comp_type.

    infile is the input file.
    outfile is the contestant's output file.
    ansfile is the standard output file.
    full_score is the maximum score.
    """
    if comp_type == 'no-extra-ws':
        if _compare_no_extra_ws(outfile, ansfile):
            return full_score
        else:
            return 0
    elif comp_type.startswith('special-judge:'):
        spj_name = comp_type[len('special-judge:'):]
        return _compare_spj(spj_name, infile, outfile, ansfile,
                            full_score)
    else:
        raise ValueError('Unknown comparison type: ' + repr(comp_type))


def _compare_no_extra_ws(out1, out2):
    """Compare file out1 and out2. Return true if two files match.

    This function ignores trailing whitespace in every line and trailing
    blank lines.
    """
    try:
        with open(out1) as f1, open(out2) as f2:
            return _compare_files_no_extra_ws(f1, f2)
    except FileNotFoundError:
        return False


def _compare_files_no_extra_ws(f1, f2):
    while True:
        l1 = f1.readline()
        l2 = f2.readline()
        if l1 == '' or l2 == '':
            # One of the files ends
            break
        if l1.rstrip() != l2.rstrip():
            return False
    while l1 != '' or l2 != '':
        if l1.rstrip() != '' or l2.rstrip() != '':
            # One of the files has a non-empty line
            return False
        l1 = f1.readline()
        l2 = f2.readline()
    return True


def _compare_spj(spj_name, infile, outfile, ansfile, full_score):
    proc = subprocess.Popen([spj_name, infile, outfile, ansfile,
                             str(full_score)],
                            stdout=subprocess.PIPE)
    proc_out, _ = proc.communicate()
    retcode = proc.poll()
    if retcode:
        return 0
    return int(proc_out)
