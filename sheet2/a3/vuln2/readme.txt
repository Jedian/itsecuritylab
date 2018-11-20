Stored XSS

There is a XSS vulnerability on the field "message" when sending a transaction
that allow us to execute javascript on the browser of both the sender and the
receiver of the transaction. To exploit it, we need to enter a '> before
<script>code</script> to close the input field and start executing scripts.

An attacker could use it to, while transfering a stupid amount of money (let's
say, 1$), make the victim who receive it, when it sees the transaction,
automatically transfer 100$ for each card it has. That is exactly what the
given python script does: create an account, log in and send a 1$ transaction
to every other card on the system with an malicious code (seen in code.js) in
the message.

To fix it, we can just add a function that makes it safer to output something
to the browser that came from the user input. This function is
"htmlspecialchars()" and to apply it is exactly what this patch does.

There is also the same kind of vulnerability in:
  -> "first name" field on "settings" page;
  -> "last name" field on "settings" page;
  -> "your message" field on "support" page;

So, as we could exploit the first two in the exact same way as we did in the
field message, and in a similar way the third, but only who could see the
message (probably the support of the webpage) would be affected, I made one
patch for all of them together.
