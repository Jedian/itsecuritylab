Kernel mode Rootkit:
This is a Loadable Kernel Module. Once loaded, it removes itself from kernel
structures to get undetectable. It supports three arguments:

hide_mod
    -> Supports a string. Search for a module with this name and makes it
    undetectable.

hide_pid
    -> Supports an integer. Search for a process with this pid and makes it
    disappear from "ps" executions.

hide_dir
    -> Supports a string. Search for a file/directory with this name and makes
    it disappear from "ls" executions.

To use it, you can execute the install.sh script available with root
privileges.
Example:

$   ./install.sh hide_mod=usb_storage hide_pid=1234 hide_dir=home



Known bugs:
If you use hide_pid, files/dirs whose name begins with pid could also disappear from
ls.
