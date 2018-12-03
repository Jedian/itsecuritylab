#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>

typedef int (*_readlink)(const char *pathname, char *buf, size_t bufsiz);

typedef int (*_open)(const char *pathname, int flags);
typedef int (*_write)(int fd, const void *buf, size_t count);
typedef int (*_read)(int fd, void *buf, size_t count);

typedef FILE* (*_fopen)(const char *pathname, const char *mode);
typedef size_t (*_fwrite)(const void *ptr, size_t size, size_t nmemb, FILE *stream);
typedef size_t (*_fread)(void *ptr, size_t size, size_t nmemb, FILE *stream);

// open
// write
// read
//
// fopen
// fwrite
// fread
//
// fgets
// fputs
//
// fprintf
// fscanf
//
// fputc
// fgetc

int readable(const char *pathname){
    char line[1024];
    _fopen orig_fopen;
    orig_fopen = (_fopen) dlsym(RTLD_NEXT,"fopen");
    FILE* wl = orig_fopen("whitelistread.txt", "r");
    while(fgets(line, sizeof(line), wl) > 0){
        int diff = strcmp(line, pathname);
        if(diff == 0 || diff == 10){ //'\n'
            fclose(wl);
            return 1;
        }
    }
    fclose(wl);
    return 0;
}

int writable(const char *pathname){
    char line[1024];
    _fopen orig_fopen;
    orig_fopen = (_fopen) dlsym(RTLD_NEXT,"fopen");
    FILE* wl = orig_fopen("whitelistwrite.txt", "r");
    while(fgets(line, sizeof(line), wl) > 0){
        int diff = strcmp(line, pathname);
        if(diff == 0 || diff == 10){ //'\n'
            fclose(wl);
            return 1;
        }
    }
    fclose(wl);
    return 0;
}


int open(const char *pathname, int flags, ...){
    _open orig_open;
    printf("SANDBOX: Opening %s.\n", pathname);
    if(!readable(pathname) && !(flags & O_RDONLY || flags & O_RDWR)){
        printf("SANDBOX: DENIED\n");
        return fileno(stdin); //stdin
    }
    if(!writable(pathname) && !(flags & O_WRONLY || flags & O_RDWR)){
        printf("SANDBOX: DENIED\n");
        return fileno(stdout); //stdout
    }
    orig_open = (_open) dlsym(RTLD_NEXT,"open");
    return orig_open(pathname,flags);
}

int write(int fd, const void *buf, size_t count){
    char flnm[1024] = "";
    char ptnm[1024] = "";
    _readlink orig_rdlink;
    _write orig_write;

    orig_rdlink = (_readlink) dlsym(RTLD_NEXT,"readlink");
    orig_write = (_write) dlsym(RTLD_NEXT,"write");
    sprintf(ptnm, "/proc/self/fd/%d", fd);

    orig_rdlink(ptnm, flnm, sizeof(flnm));

    printf("SANDBOX: Write requested at %s\n", flnm);
    if(!writable(flnm)){
        printf("SANDBOX: DENIED\n");
        return 0; // return success so suspicious application will continue execution
    }
    return orig_write(fd, buf, count);
}

int read(int fd, void *buf, size_t count){
    char flnm[1024] = "";
    char ptnm[1024] = "";
    _readlink orig_rdlink;
    _read orig_read;

    orig_rdlink = (_readlink) dlsym(RTLD_NEXT,"readlink");
    orig_read = (_read) dlsym(RTLD_NEXT,"read");
    sprintf(ptnm, "/proc/self/fd/%d", fd);

    orig_rdlink(ptnm, flnm, sizeof(flnm));

    printf("SANDBOX: Read requested at %s\n", flnm);
    if(!readable(flnm)){
        printf("SANDBOX: DENIED\n");
        return 0; // return success so suspicious application will continue execution
    }
    return orig_read(fd, buf, count);
}

FILE *fopen(const char *path, const char *mode){
    _fopen orig_open;
    printf("SANDBOX: FOpening %s.\n", path);
    if(!readable(path) && (mode[0] == 'r' || mode[1] == '+')){
        printf("SANDBOX: DENIED\n");
        return stdin;
    }
    if(!writable(path) && (mode[0] == 'w' || mode[0] == 'a' || mode[1] == '+')){
        printf("SANDBOX: DENIED\n");
        return stdout;
    }
    orig_open = (_fopen) dlsym(RTLD_NEXT,"fopen");
    return orig_open(path, mode);
}

size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream){
    char flnm[1024] = "";
    char ptnm[1024] = "";
    _readlink orig_rdlink;
    _fwrite orig_fwrite;

    orig_rdlink = (_readlink) dlsym(RTLD_NEXT,"readlink");
    orig_fwrite = (_fwrite) dlsym(RTLD_NEXT,"fwrite");
    sprintf(ptnm, "/proc/self/fd/%d", fileno(stream));

    orig_rdlink(ptnm, flnm, sizeof(flnm));

    printf("SANDBOX: FWrite requested at %s\n", flnm);
    if(!writable(flnm)){
        printf("SANDBOX: DENIED\n");
        return 0; // return success so suspicious application will continue execution
    }
    return orig_fwrite(ptr, size, nmemb, stream);
}

size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream){
    char flnm[1024] = "";
    char ptnm[1024] = "";
    _readlink orig_rdlink;
    _fread orig_fread;

    orig_rdlink = (_readlink) dlsym(RTLD_NEXT,"readlink");
    orig_fread = (_fread) dlsym(RTLD_NEXT,"fread");
    sprintf(ptnm, "/proc/self/fd/%d", fileno(stream));

    orig_rdlink(ptnm, flnm, sizeof(flnm));

    printf("SANDBOX: FRead requested at %s\n", flnm);
    if(!readable(flnm)){
        printf("SANDBOX: DENIED\n");
        return 0; // return success so suspicious application will continue execution
    }
    return orig_fread(ptr, size, nmemb, stream);
}
