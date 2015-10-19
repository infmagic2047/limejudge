"""Find a source file and compile it into a executable."""

import os
import shlex
import shutil
import subprocess


class CompileError(Exception):
    """Failed to compile a source file."""


class CompilerNotFoundError(CompileError):
    """Cannot find compiler."""


class NoSourceFileError(Exception):
    """Cannot find source file to compile."""


def _compile_command(cmdline):
    if shutil.which(cmdline[0]) is None:
        raise CompilerNotFoundError('Cannot find ' + cmdline[0])
    proc = subprocess.Popen(cmdline,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    proc_out, _ = proc.communicate()
    retcode = proc.poll()
    if retcode:
        raise CompileError(cmdline[0] + ' failed', proc_out)


def compile_c_into(src, dst, extra_flags=None):
    if extra_flags is None:
        extra_flags = []
    _compile_command(['gcc', src, '-o', dst] + extra_flags)


def compile_cpp_into(src, dst, extra_flags=None):
    if extra_flags is None:
        extra_flags = []
    _compile_command(['g++', src, '-o', dst] + extra_flags)


FILETYPE_HANDLERS = {
    'c': compile_c_into,
    'cpp': compile_cpp_into,
}

DEFAULT_FILETYPES = ['c', 'cpp']


def compile_into(src, dst, filetypes=None, compiler_flags=None):
    """Compile src.* into dst.

    filetypes indicate what file extensions to try for src. Raise
    CompileError when compilation failed. Raise NoSourceFileError when
    no available source files are found.
    """
    if filetypes is None:
        filetypes = DEFAULT_FILETYPES
    if compiler_flags is None:
        compiler_flags = {}
    for ft in filetypes:
        src_file = src + '.' + ft
        if os.path.isfile(src_file):
            flags = compiler_flags.get(ft, '')
            flags_list = shlex.split(flags)
            FILETYPE_HANDLERS[ft](src_file, dst, flags_list)
            return
    raise NoSourceFileError
