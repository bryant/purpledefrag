#define MAX_CVARS 1024
#define FILE_HASH_SIZE 256

#define CVAR_LIST_SIZE (sizeof(cvar_t) * MAX_CVARS)
#define CVAR_INDEX_SIZE (sizeof(unsigned int) * FILE_HASH_SIZE)
#define SHM_SIZE (CVAR_LIST_SIZE + CVAR_INDEX_SIZE)

typedef enum {qfalse, qtrue}	qboolean;

typedef struct cvar_s {
	char			name[64];
	char			string[256];
	char			*resetString;		// cvar_restart will reset to this value
	char			*latchedString;		// for CVAR_LATCH vars
	int				flags;
	qboolean	modified;			// set each time the cvar is changed
	int				modificationCount;	// incremented each time the cvar is changed
	float			value;				// atof( string )
	int				integer;			// atoi( string )
	qboolean	validate;
	qboolean	integral;
	float			min;
	float			max;
	struct cvar_s *next;
	unsigned int hashNext;
} cvar_t;

long hash(const char *n);
cvar_t *find(const char *name, cvar_t *list, unsigned int *index);
