Title: Unicode and command line flag parsing
Date: 2020-07-22 21:35:00
Author: David Wilemski
Category: blog
Tags: programming
Slug: unicode-cli-flag-parsing
Status: published

Yesterday I read [Dealing with Non-ASCII Characters](https://blog.jpalardy.com/posts/dealing-with-non-ascii-characters/) and the talk about curly quotes copied and pasted from Google Docs or Slack reminded me of a "fun" problem that I used to have to deal with occasionally that was along similar lines. It had to do with copying and pasting a full command line invocation complete with flags and arguments out of a tool that was commonly used on a project I was working on. Maybe you'd paste in a fully formed command as an example into a design or a set of FAQs or something – however when someone copied and pasted it back out a flag that might've been `--debug` turned into `—debug`. In other words, the double hyphen was getting turned into an em-dash.

Alone, this isn't really a huge problem but might not work as expected. If you use some certain command line parsing libraries/frameworks that make your life easier in other ways, then this situation might result in failures or maybe even an unhandled exception and a stack trace being spewed out pointing at parsing code that's inside of the framework where it's reading `argv`.

What to do?

Depending on the library being used and exactly how it parses the parameters, there may not be an easy way to handle exceptions like this from within the framework. You might have to wrap your call that "enters" the framework in your `main` function with some exception handling in order to be able to avoid these unhandled exceptions. Then you could provide a specialized "are you sure you used valid ASCII characters in your command?" error message. However, as Julia Evans points out: [unicode is valid in command line arguments](https://wizardzines.com/comics/command-line-arguments/)! Unfortunately I don't really have any fix to offer for this situation if your framework doesn't catch it for you. This post is more a word of warning in case you or someone you know comes to you asking what's going on with a command that was copied and pasted from elsewhere – I had to debug this for people a number of times in the past. Probably the easiest "fix", if you can change the place the command was copied from, is to ensure double dashes weren't "helpfully" turned into an em-dash.

Jonathan provided a cool regex at the end of his post though. It will help with detecting non-ASCII characters and describes a trick for remembering the visible range of the ASCII table. It won't help with the exact situation I describe above but if you're trying to figure out why some JSON you copied and pasted is now invalid or something, it's definitely worth keeping in mind.


