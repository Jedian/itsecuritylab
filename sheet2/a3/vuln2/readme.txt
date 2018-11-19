Stored XSS

There is a XSS vulnerability on the field "message" when sending a transaction
that allow us to execute javascript on the browser of both the sender and the
receiver of the transaction. To exploit it, we need to enter a '> before
<script>code</script> to close the input field and start executing scripts.

An attacker could use it to, while transfering a stupid amount of money (let's
say, 1$), make the victim who receive it, when it sees the transaction,
automatically transfer 100$ for each card it has. That is exactly what the
given python script does: create an account, log in and send a 1$ transaction
to every other card on the system.
