#include <iostream>

#include <Python.h>

static PyObject* f( PyObject* self, PyObject* args ) {
    std::cout << "Hello, from C++!" << std::endl;
    Py_RETURN_NONE;
}

static PyMethodDef methods[] = {
    { "f",  f, METH_VARARGS, "First f" },
    { NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC initb3( void ) {
    PyObject* m = Py_InitModule( "b3", methods );
}
