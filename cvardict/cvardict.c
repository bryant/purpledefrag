#include <Python.h>
#include <sys/mman.h>
#include <fcntl.h>
#include "cvardict.h"
#include "cvshm.h"


static PyMethodDef module_methods[] = {
	{NULL}
};

static PyMappingMethods CvarDictMap = {
	.mp_subscript = (binaryfunc)CvarDict_getitem,
};

static PyTypeObject CvarDictType = {
	PyObject_HEAD_INIT(NULL)
	.tp_name = MODULE_NAME ".CvarDict",
	.tp_basicsize = sizeof(CvarDict),

	.tp_dealloc = (destructor)CvarDict_dealloc,
	.tp_new = CvarDict_new,
	.tp_init = (initproc)CvarDict_init,

	.tp_as_mapping = &CvarDictMap,

	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
};

static PyObject *CvarDict_new(PyTypeObject *type,
	PyObject *args, PyObject *kwds) {

	CvarDict *self;

	self = (CvarDict *)type->tp_alloc(type, 0);
	self->size = 0;
	self->start = NULL;
	self->file = NULL;
	self->fd = -1;

	return (PyObject *)self;
}


static int CvarDict_init(CvarDict *self, PyObject *args) {
	struct stat f;

	if (PyArg_ParseTuple(args, "s", &(self->file)) == 0) {
		return -1;
	}

	self->fd = shm_open(self->file, O_RDONLY, 0);
	if (self->fd == -1) {
		PyErr_SetFromErrno(PyExc_IOError);
		return -1;
	}

	if (fstat(self->fd, &f) != 0) {
		PyErr_SetFromErrno(PyExc_IOError);
		return -1;
	}

	self->size = f.st_size;
	self->start = mmap(NULL, self->size, PROT_READ, MAP_SHARED,
		self->fd, 0);
	if (self->start == MAP_FAILED) {
		PyErr_SetFromErrno(PyExc_MemoryError);
		return -1;
	}

	return 0;
}

static void CvarDict_dealloc(CvarDict *self) {
	if (self->start) {
		munmap(self->start, self->size);
	}

	close(self->fd);
}

static PyObject *CvarDict_getitem(CvarDict *self, PyObject *key) {
	char *ckey;
	cvar_t *match;

	if (!PyString_Check(key)) {
		PyErr_SetString(PyExc_KeyError, "Cvar names must be strings");
		return NULL;
	}

	ckey = PyString_AsString(key);
	match = find(ckey, (cvar_t *)self->start,
		(unsigned int *)(self->start + CVAR_LIST_SIZE));

	if (match == NULL) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	return PyString_FromString(match->string);
}

PyMODINIT_FUNC initcvardict(void) {
	PyObject *m;

	if (PyType_Ready(&CvarDictType) < 0) {
		return;
	}

	m = Py_InitModule(MODULE_NAME, module_methods);
	if (m == NULL) {
		return;
	}

	Py_INCREF(&CvarDictType);
	PyModule_AddObject(m, "CvarDict", (PyObject *)&CvarDictType);
}
