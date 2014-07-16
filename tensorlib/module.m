#import <Foundation/Foundation.h>
#import <Python.h>

#import "filters.h"

/*
 * Stub python module declaration --
 * Allows Objective-C classes with which it is linked
 * to be found and loaded from python via `objc.lookUpClass()`
 */

static PyObject *TensorlibError;
static PyMethodDef methods[] = {
    { NULL, NULL },
};

PyMODINIT_FUNC
inittensorlib(void) {
    PyObject *module;
    
    module = Py_InitModule("tensorlib", methods);
    TensorlibError = PyErr_NewException("tensorlib.error", NULL, NULL);
    Py_INCREF(TensorlibError);
    PyModule_AddObject(module, "error", TensorlibError);
}

