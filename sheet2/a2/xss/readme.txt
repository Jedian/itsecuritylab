Cross-Site Scripting:
There are XSS vulnerabilities within:
-> Sending/reading messages.
-> Writing/reading pinboard texts.
-> Editing/reading fields on an user profile (About me).

All of them allows us to execute javascript on other people's browser.
I wrote a code that capture the victim's cookies and send them to Hanni Ball
via message. To use it, Hanni Ball has to post the script on a friend's
pinboard, send it through message to someone, or even hide it in it's own
profile. When someone logged in access the page with this script, a message is
sent from that user to Hanni Ball with the person cookies, that can be used by
Hanni Ball to access the application with their account.
