Improper auth validation

After registered and logged in, in the transactions webpage, inspecting the
source code, I found a hidden field with the user id. It is possible to change
it to 1, for instance. (The id of support (admin)). On doing that, we get a
list with all the transactions of any other user.

Note: Every transaction of user "support" contains a flag as message.

The patch makes the field and therefore, the vulnerability also, useless,
because after it, the transactions gathered are from the id of the user whose
session is active (logged in).

The script gets, through the vulnerability, the list of all transactions
from/to user "support", whose id is 1. I found a flag in every of these
transactions and they are printed on the outcome of the script.
