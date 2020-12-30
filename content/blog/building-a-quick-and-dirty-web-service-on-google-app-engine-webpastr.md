Title: Building a quick and dirty web service on Google app engine: WebPastr
Date: 2010-10-09 14:14:00
Author: David Wilemski
Tags: Web Dev
Category: blog
Slug: building-a-quick-and-dirty-web-service-on-google-app-engine-webpastr
Status: published
Attachments: blog/wp-content/uploads/2010/10/Alfred-Preferences.jpg, blog/wp-content/uploads/2010/10/Google-Chrome.jpg

Update (5/26/2011): I've now [open sourced the
code](http://github.com/davidwilemski/webpastr) and [wrote a little more
about
WebPastr](http://oromis.davidwilemski.com/blog/191/webpastr-revisited/)

[Earlier this
week](http://twitter.com/#!/davidwilemski/status/26662857425) I though
that it would be nice to post a text snippet to
[PasteBin](http://pastebin.com/) via [Alfred](http://alfredapp.com) on
my Mac. I looked into how a new pastebin post is posted and was dismayed
by the fact that I couldn't set it up just with Alfred's wonderful
custom search feature.

Last night I decided to build a quick [app
engine](http://code.google.com/appengine/) application as an
intermediate step between me and PasteBin.

I've done a little (unpublished) work with Python on app engine before
so I quickly chose that as my language. I knew enough to get me going. I
had to write a main page (this still must be done) and the script that
would handle my requests and forward them on to PasteBin.

I am happy to say that in under an hour I got it working with a very
rough set of features; Namely, posting to PasteBin. I have tested that
this works if you setup a custom search inside of both Alfred and Google
Chrome. I have posted some screenshots of the settings windows for each
app here.

One of the things I keep hearing from both people who work at startups
and even presenters from Google is to actually release something, to
build and iterate. Â Even though I don't even have a webpage designed
for the service yet there are no other features yet, I am releasing
this. This is not something I would have done before.

In order to create a new post you send a request to this URL:
[http://webpastr.appspot.com/post?code={yourtexthere}](http://webpastr.appspot.com/post?code=%7Byourtexthere%7D)

\[caption id="attachment\_95" align="alignleft" width="300"
caption="Alfred
Preferences"\][![](http://oromis.davidwilemski.com/blog/wp-content/uploads/2010/10/Alfred-Preferences-300x89.jpg
"Alfred Preferences")](http://oromis.davidwilemski.com/blog/wp-content/uploads/2010/10/Alfred-Preferences.jpg)\[/caption\]

\[caption id="attachment\_96" align="alignleft" width="300"
caption="Chrome
Preferences"\][![](http://oromis.davidwilemski.com/blog/wp-content/uploads/2010/10/Google-Chrome-300x136.jpg
"Google Chrome")](http://oromis.davidwilemski.com/blog/wp-content/uploads/2010/10/Google-Chrome.jpg)\[/caption\]

What are my plans for the future of
[WebPastr](http://webpastr.appspot.com)?

First, I'd like to support other services. Definitely
[Gist](http://gist.github.com/) when [GitHub](http://Github.com) finally
allows the API to post new Gists.

I'd also like to support PasteBin's post expiration feature.

Lastly, I plan on designing a homepage for the app that clearly explains
how to use it in various applications. I believe I could easily get
Firefox working with this and maybe a Bash script as well.

Feel free to use this now, and be on the lookout for new features soon\!
