Title: MCommunity XSS
Date: 2011-08-12 22:31
Author: David Wilemski
Tags: Security, Web Dev
Category: blog
Slug: mcommunity-xss
Status: published
Attachments: blog/wp-content/uploads/2011/08/mcommunity.png, blog/wp-content/uploads/2011/08/mcommunity-1.png

The University of Michigan [recently
launched](http://michigandaily.com/news/u-launches-new-directory-program-mcommunity)
a new directory site called
[MCommunity](http://mcommunity.umich.edu)Â that is to be used to
search for information on people related to theÂ University.

A few days after the site launched my friendÂ [Bryan
Kendall](http://bryankendall.com) found a persistent XSS vulnerability
in MCommunity within a couple minutes of looking at the site. He
reported the problem to the Michigan security team.

# ...Or how I almost wormed MCommunity

Days passed and I got curious about how MCommunity itself worked as it
obviously used a lot of AJAX to load information on pages. So I took a
look at what those calls looked like using Chrome's developer tools. It
looks as though MCommunity is sitting on top of a pretty nice JSON API\!
They included endpoints for gathering info on an account, the current
user's auth info, and various other endpoints including the one for
updating a profile.

So what did I do? I wanted to update my own profile via XSS of course -
just to see how it worked. I embedded a Javascript snippet in the alt
address field that Bryan found was vulnerable that loaded an [external
script](http://davidwilemski.com/static/js/mcommunity_xss/mcommunity_profileedit.js)
hosted on my server.

\[caption id="attachment\_220" align="alignleft" width="391"
caption="Screenshot of the snippet in the form before I submitted
it"\][![](http://oromis.davidwilemski.com/blog/wp-content/uploads/2011/08/mcommunity.png
"mcommunity")](http://oromis.davidwilemski.com/blog/219/mcommunity-xss/mcommunity/)\[/caption\]

That external script simply made some AJAX calls to various endpoints
with the purpose of updating the user who was viewing my profile's Alt.
Phone number to "I have you now". This was accomplished by grabbing the
user's authentication information and posting to the proper place;
because the Javascript was being executed in the context of a logged in
user it posted their existing auth cookie along with the post and acted
on behalf of the user but without their permission.

\[caption id="attachment\_221" align="alignleft" width="205"
caption="Screenshot of the modified field on my profile after being
XSS'd by
myself"\][![](http://oromis.davidwilemski.com/blog/wp-content/uploads/2011/08/mcommunity-1.png
"mcommunity-1")](http://oromis.davidwilemski.com/blog/219/mcommunity-xss/mcommunity-1/)\[/caption\]

After testing this to see if it worked with a couple of friends (letting
them know what would happen before hand), I stopped loading that script
into my profile so as not to actually modify anyone else's data. I
replaced it with a simple alert that said that MCommunity was vulnerable
and that concerned users should notify the University.

Had I been malicious, I could have modified others' profiles so that
when they were viewed, they too would attack other people's profiles.
This worm could have spread out of control and caused much grief. There
are also any number of other things that an attacker could do with an
open XSS bug. This is why testing for these things in development is so
important.

# Response

I promptly reported the vulnerability as well because I didn't want
others doing this to me\! I quickly got a response from the security
team saying they had passed it on to the MCommunity team. About a week
later, on August 2nd, Â I noticed that the vulnerability had been fixed
and no longer worked. They must have patched it in one of [these
releases](http://www.itcs.umich.edu/mcommunity/releasenotes/directory/July2011.php)Â -
despite not mentioning it in those notes.

Overall the response from the University was very good. I do hope that
they are on the lookout for further vulnerabilities in the application.
It houses so much information on the entire Michigan community that it
would be disappointing to see that be abused by a malicious attacker.
