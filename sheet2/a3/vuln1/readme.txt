Improper auth validation

After registered and logged in, in the transactions webpage, inspecting the
source code, I found a hidden field with the user id. It is possible to change
it to 1, for instance. (The id of support (admin)). On doing that, we get a
list with all the transactions of any other user.

Note: Every transaction of user "support" contains a flag as message.
