Task 1 - Service fingerprinting
Language: Python 2.7
File: service_fingerprinter.py
Usage: ./service_fingerprinter.py <HOST>

Dependencies:
  python2.7 - apt-get install python2.7-dev
  requests - pip install requests


This script will scan every port in host HOST, trying to connect to it through
a socket. If it succeeds, there is a service listening to it on the target host
and we can try to fingerprint it.
My implementation only covers some HTTP and FTP daemons:
  * Those HTTP daemons which send their own service's name/version through
  "Server" header on HTTP responses.
  * Those FTP daemons specified on the assignment: vs-ftpd, pro-ftpd, py-ftpd,
  pure-ftpd. I did this by connecting to them and sending a HELP command. Every
  one of them answered in a different way, allowing me to match it with a small
  database of typical answers to fingerprint them.

This implementation could be easily enriched by enlarging the database, and by
adding more commands able to distinguish different daemons.

A successful run using as target host the course vpn host "10.0.23.15" can be
seen in the file "run_example.txt".

There, we can gather the information to answer the questions in the assignment
sheet:

1) There are actually 100 HTTP daemons on 100 different ports, but there are
only 5 different services, so every service appears 20 times:
  * Apache/2.4.7 (Ubuntu)
  Ports: 2589, 8223, 9813, 10423, 15302, 17773, 18824, 20545, 23439, 23955,
  31711, 36798, 37707, 39207, 40074, 40642, 40671, 52381, 56662, 64065.

  * mini_httpd/1.19 19dec2003
  Ports: 777, 1408, 4739, 11901, 14673, 18254, 22012, 28975, 31331, 40305,
  42037, 44113, 48915, 50525, 50844, 52028, 56617, 61210, 61299, 64947.

  * micro_httpd
  Ports: 3890, 6966, 12346, 15047, 18948, 24542, 28072, 29058, 38603, 41347,
  46382, 49241, 51250, 51359, 53999, 57311, 58689, 61556, 64220, 64442.

  * webfs/1.21
  Ports: 5533, 12080, 16663, 18769, 27890, 38090, 40110, 47963, 48870, 50187,
  50318, 50356, 50775, 52347, 53559, 53968, 59480, 60284, 60346, 60835.

  * lighttpd/1.4.33
  Ports: 6371, 8486, 10388, 13967, 20863, 21241, 22461, 23255, 24584, 25797,
  26378, 33210, 33922, 36424, 38591, 40126, 42715, 52867, 55159, 56900.

2)* Port 210:   ProFTPd
  * Port 2100:  Pure-FTPd
  * Port 2121:  PyFTPd
  * Port 21000: vsFTPd

