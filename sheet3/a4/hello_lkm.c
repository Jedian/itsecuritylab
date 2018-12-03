#include<linux/module.h>
#include<linux/init.h>
#include<linux/kernel.h>

MODULE_LICENSE("GPL");

static int __init module_load(void)
{
    printk("HelloLKM\n");
    return 0;
}
static void __exit module_unload(void)
{
    printk("GoodbyeLKM\n");
}

module_init(module_load);
module_exit(module_unload);
