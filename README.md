## Secret Santa

Run:

```console
$ python secret_santa.py Alice Bob Charlie ...
```

This will generate a folder `out/` looking like this:

```
215f91.html
883fc0.html
d36598.html
```

All that's left to do is to deploy the HTML files somewhere
(but *without* directory index!) - and sent the URLs
to each participants.

They cannot guess the URLs for the other participants, and as
long as _you_ don't click on the 'summary', you don't know
any secrets either.
