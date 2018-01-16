Title: How MCommunity Works
Date: 2011-08-17 02:05
Author: David Wilemski
Category: Web Dev
Slug: how-mcommunity-works
Status: published

In my [last
post](http://oromis.davidwilemski.com/blog/219/mcommunity-xss/ "MCommunity XSS"),
I briefly mentioned that I thought MCommunity was sitting on a pretty
nice JSON API. Today, I\'ll be covering some of the endpoints that I
mentioned and what the data looks like when it comes back. I\'m writing
this not because it was particularly difficult to figure out - anyone
with a web browser can do it quickly with the developer tools - but
because I enjoyed getting a glimpse into how the service was structured.

When I first looked at it, MCommunity had an endpoint that the
Javascript was POSTing to to get details about who was logged in.  
Doing a GET to
https://mcommunity.umich.edu/mcPeopleService/private/people/getAuthorization/dummy
will give a few details about the user who is currently signed in. For
instance, when I am signed in, mine looks like:

    {
        "authcheck": {
            "errors": "",
            "authStatus": true,
            "displayName": "David Thomas Wilemski Jr",
            "dn": "uid=dtwilems,ou=people,dc=umich,dc=edu",
            "elevatedStatus": false,
            "uniqname": "dtwilems"
        }

    }

**Note:** They\'ve since stopped using the \"dummy\" signifier in place
of some sort of numerical ID; My guess is that it was an attempt to
change that endpoint per session so it wouldn\'t be so easy to call.
However, \"dummy\" still works as does any integer - and most strings
too. Maybe it was changed for some other reason, I guess I\'ll never
know.

As you can see, this is very useful information when exploiting XSS. It
tells you exactly which user is currently authenticated. While the XSS
vulnerability was still present, I could have written a script to notify
me when someone viewed my profile and tell me exactly who was viewing
it. Furthermore, because the script would have been executing in the
context of the other user, it could have used the next endpoint that
I\'ll be discussing to ask for all of a user\'s personal information
that is stored in MCommunity and send that to a malicious attacker.
That\'s some serious analytics.

The next endpoint gives information for a uniqname based on who the user
asking for it is. For instance, the URL:  
https://mcommunity.umich.edu/mcPeopleService/private/people/dtwilems  
gives info on me! Here is what I see when I view the page:

    {
        "person": {
            "distinguishedName": "uid=dtwilems,ou=people,dc=umich,dc=edu",
            "errors": "",
            "aboutMeView": 2,
            "acl": [
                "3#entry#ou=People,dc=umich,dc=edu#drink",
                "3#entry#ou=People,dc=umich,dc=edu#umichAltPhone",
                "3#entry#ou=People,dc=umich,dc=edu#umichAltAddress"
            ],
            "affiliation": [
                "College of Engineering - Faculty and Staff",
                "CoE-IT - Faculty and Staff",
                "Undergraduate Engineering - Student",
                "Alumni"
            ],
            "aliases": [
                "David Thomas Wilemski",
                "David Wilemski Jr",
                "David Wilemski",
                "David T Wilemski",
                "David Thomas Wilemski Jr"
            ],
            "altAddressView": 1,
            "altPhoneView": 1,
            "associatedDomain": "engin.umich.edu",
            "displayName": "David Thomas Wilemski Jr",
            "drink": "Cranberry Juice",
            "email": "dtwilems@umich.edu",
            "emailForwarding": [
                "dtwilems@mail.umich.edu",
                "dtwilems.umich@gmail.com",
                "dtwwtd@gmail.com"
            ],
            "faxPhoneView": 2,
            "ferpa": "N",
            "homeAddressView": 2,
            "homePhoneView": 2,
            "imView": 2,
            "mobilePhone": "------MY CELL NUMBER-------",
            "mobilePhoneView": 2,
            "noticeView": 2,
            "pagerPhoneView": 2,
            "permanentAddress": "-------PLACE WHERE I LIVE--------",
            "spamFilter": "TRUE",
            "title": "Student, Undergraduate Engineering",
            "uniqname": "dtwilems",
            "urlView": 2,
            "vacationView": 2
        }
    }

 

However, if I call the API for someone else\'s info then it only returns
information that they have marked as public. Well, actually, you can
mark things as public, or just viewable to logged in users (auth), or
private (self). They actually return information structured pretty well,
and as we\'ll see, I\'ve since discovered more API endpoints like these
- but first I\'d like to talk about the last endpoint that I used while
digging around with the XSS exploit.

This is the one that really made things go. POSTing to this with the
correct variables and a valid cookie will update a profile:

https://mcommunity.umich.edu/mcPeopleService/private/people/updateContact

This is the one that could have helped to cause the [MySpace
worm](http://namb.la/popular/) of MCommunity - if I was evil. Instead, I
reported it like any upstanding Michigan community member would have. :D

Conclusion
==========

So, like I said, the MCommunity site has a nice API. As a matter of
fact, [Bryan](http://bryankendall.com) and I have just discovered some
various
[WADL](http://en.wikipedia.org/wiki/Web_Application_Description_Language)
files that describe additional endpoints. I\'ll list the ones we know
about out now for some of you curious folk:

-   https://mcommunity.umich.edu/mcPeopleService/
-   https://mcommunity.umich.edu/mcDirectoryMessages/
-   https://mcommunity.umich.edu/mcGroupService/

What would I like to see MCommunity do with its API? Open it up! I mean,
we\'re a top computer science school for crying out loud! I think that
the students and alumni here could do some truly amazing things if this
were to be opened up and documented a little better. Actually, this is
something I think that the entire University could do better.
Initiatives like the [Mobile Center](http://mobile.umich.edu/) are great
but the applications that they put out are still purely proprietary. In
fact, their [APIs page](http://mobile.umich.edu/dev/apis) has had
basically a \"coming soon\" message on it for over a year now.

As it is, any student who wants to build a mobile or web application
related to the University is usually forced to revert to lame attempts
at scraping a web page for information and other gross, hackish things
in order to get functionality out of their application. I\'ve
experienced this first hand with both [Umich
Dining](http://davidwilemski.com/umichdining) and
[MSchedule](http://mschedule.com). We actually found computer readable
formats for both of those applications but not without some exploring
first. The data feeds aren\'tÂ advertisedÂ in any way and I think that
they need to be. I\'ve heard very similar stories over and over from
other students who have tried to build some Michigan specific
application at a hackathon or for other purposes and, honestly, it gets
frustrating.

I will say that it seems that the University is getting better at trying
to support development here on campus - we\'re just not quite there yet.
If anyone who works for the University who can help move this along is
reading, just know that you\'re moving in the right direction - we just
want you to get there faster!

Also, us MSchedule developers would like to be able to register users
for classes so as to create a much better user experience. Pipe dreams,
we know\...
