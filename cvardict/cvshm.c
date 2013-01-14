#if defined(STANDALONE)
#include <sys/mman.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#endif

#include <strings.h>
#include <ctype.h>
#include "cvshm.h"


long hash(const char *n) {
	int i;
	long hash = 0;

	for (i = 0; n[i]; i++) {
		hash += (long)tolower(n[i]) * (i + 119);
	}

	return hash & (FILE_HASH_SIZE - 1);
}

cvar_t *find(const char *name, cvar_t *list, unsigned int *index) {
	cvar_t	*var;
	unsigned int current;

	for (current = index[hash(name)];
		current != -1 ; current = var->hashNext) {

		var = &(list[current]);
		if (!strcasecmp(name, var->name)) {
			return var;
		}
	}

	return (void *)0;
}

#if defined(STANDALONE)
main(void) {
	printf("sizeof cvar_t = %d\n", sizeof(cvar_t));

	int fd = shm_open("/openarena:24353", O_RDONLY, 0);

	if (fd == -1) {
		printf("shm_open failed\n");
		return -1;
	}

	struct stat b;
	if (fstat(fd, &b) != 0) {
		printf("fstat failed\n");
		goto gtfo;
	}

	if (b.st_size != SHM_SIZE) {
		printf("shmem is %d bytes, expected %d\n", b.st_size, SHM_SIZE);
		goto gtfo;
	}

	void *shm = mmap(0, b.st_size, PROT_READ, MAP_SHARED, fd, 0);
	if (cvarlist == MAP_FAILED) {
		printf("mmap failed\n");
		goto gtfo;
	}

	cvarlist = (cvar_t *)shm;
	cvarindex = (unsigned int *)(shm + CVAR_LIST_SIZE);

	unsigned int i;
	cvar_t *f;
	
	for (i = 0; i < MAX_CVARS; i++) {
		f = &(cvarlist[i]);
		printf("#%d: %s = %s\n", i, f->name, f->string);
	}

	printf("string @ 0x1310: %s\n", (char*)(shm + 0x1310));

	cvar_t *promode = find("df_promode");
	if (promode == 0) {
		printf("Couldn't find promode\n");
	}
	else {
		printf("Found it: %s = %s\n", promode->name, promode->string);
	}

	munmap(cvarlist, b.st_size);

gtfo:
	close(fd);
}
#endif
