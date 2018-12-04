ICMP Reverse shell backdoor:
After setted up and installed, the script slave.py will be running with root
privileges on the target machine, sending ICMP requests to the attacker
machine, notifying it that it is ready to send back a reverse shell.

Once ready, when the attacker wants to get access to it, it has to run the
script master.py, that listens these requests and send a pre-setted password.
If it's correct, the backdoor will start to listen for shell commands and send
back their executions as root on the target machine.

The entire communication is implemented using ICMP.

Setting up:

Edit the file const.py with the address of the attacker host and the password.

Installing:

Execute the script install.sh with root privileges.

Running:

When you want to get remote access, execute the master script on the attacker
host.
