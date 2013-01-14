#define MODULE_NAME "cvardict"

typedef struct {
	PyObject_HEAD

	size_t size;
	void *start;
	char *file;
	int fd;
} CvarDict;

static PyObject *CvarDict_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int CvarDict_init(CvarDict *self, PyObject *args);
static void CvarDict_dealloc(CvarDict *self);
static PyObject *CvarDict_getitem(CvarDict *self, PyObject *key);
