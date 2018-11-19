Improper Authentication:
Analyzing the critical source code, we can check that the Inbox and the Outbox
messages are gathered from the database through the first name of the logged in
user, rather than it's ID or something unique. The same happens with the
Sprayers list, but with the user's email. So we can get them just by
registering a new user with the same first name and email to read all of it.
And that is exactly what I did to get it:

inbox:

> From: Hanni Ball
  Subject: Re: Football
  Message: Nobody in football should be called a genius. A genius is a guy like Norman Einstein!

> From: Hanni Ball
  Subject: Re: discotheque tonight
  Message: Drink 'till she's cute, but stop before the wedding.

outbox:

> To: Isaac Cox
  Subject: No subject
  Message: I say no to drugs, but they don't listen.

> To: General E. Speaking
  Subject: notice
  Message: If you have noticed this notice you will have noticed that this notice is not worth noticing.

sprays:

> AI Dente sprayed you.
> Mammoth Erections sprayed you.
> Marsha Mellow sprayed you.
> Hanni Ball sprayed you.
> Isaac Cox sprayed you.
> General E. Speaking sprayed you.
> April Schauer sprayed you.
> Gaylord Perry sprayed you.

