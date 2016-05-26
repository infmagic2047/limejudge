#include <Python.h>

#include <sys/ptrace.h>

static PyObject *ptrace_traceme(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, "")) {
        return NULL;
    }

    long result = ptrace(PTRACE_TRACEME, 0, NULL, NULL);

    if (result == -1) {
        return PyErr_SetFromErrno(PyExc_OSError);
    }

    Py_RETURN_NONE;
}

static PyObject *ptrace_syscall(PyObject *self, PyObject *args)
{
    pid_t pid;
    int signal;

    if (!PyArg_ParseTuple(args, "ii", &pid, &signal)) {
        return NULL;
    }

    long result = ptrace(PTRACE_SYSCALL, pid, NULL, signal);

    if (result == -1) {
        return PyErr_SetFromErrno(PyExc_OSError);
    }

    Py_RETURN_NONE;
}

static PyMethodDef ptrace_methods[] = {
    {"traceme", ptrace_traceme, METH_VARARGS, NULL},
    {"syscall", ptrace_syscall, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}  /* Sentinel */
};

static struct PyModuleDef ptrace_module = {
    PyModuleDef_HEAD_INIT,
    "ptrace",
    NULL,
    -1,
    ptrace_methods
};

PyMODINIT_FUNC
PyInit_ptrace(void)
{
    return PyModule_Create(&ptrace_module);
}
