Title: Why I Wrote My Own URL Shortener
Date: 2018-02-05 23:25
Author: David Wilemski
Category: blog
Slug: url-shortener
Status: draft

I wrote my own URL shortener.

## Why?
That statement might seem surprising at first but I built it for a very specific purpose: I keep a notebook as a cross between a planner, todo list, and scratch paper to keep notes. I use a modified version of the [Bullet Journal](http://bulletjournal.com/) system and wanted a way to link notes on paper to the webpages I needed to refer to for notes, ideas, and todo items. This was the core of the technical requirements but there were philosophical reasons for building my own URL shortener as well.

I wanted a URL shortener that provided as short of a URL as possible so that I could write it down on paper in my notebooks. Publicly available shortener services and open source projects generally produce fairly lengthy URLs when you’re considering hand writing them and so I came up with my own key space based on my expected usage. I’ll get to that in a moment. The philosophic reasons alluded to before were around data longevity and ownership. I go through approximately two notebooks each year and have been using this method of organization for my life and work for a few years already and don’t see that changing any time soon.

I was concerned with being able to export all URLs I’ve shortened with their keys in the case that whatever service I chose went offline. This is something I looked into before embarking on implementing my own shortener but couldn’t find anything that quelled my concerns so I spent a couple hours one weekend to get the basics implemented.

## How Is it Different?
As mentioned before, I wanted to make the short URLs as easy to write down as possible. I considered the simple approach of incrementing an integer key but quickly moved on. At first it would work very nicely but it would rather quickly reach four-digit keys, even with a low rate of use of 1-3x per day.

Instead, I considered a key space similar to that of base 64 encoding. I didn’t want to deal with non-alphanumeric characters though so I used `[a-zA-Z0-9]` which ends up being 62 characters. Next I considered how long each key would have to be so that all URLs could be of the same length. Two character keys (`62^2` or 3,844) might have lasted a few years but would have eventually run out. Three character keys (`62^3` or 238,328) seemed likely to cover me for as long as I wanted since my usage pattern would be manually generated short URLs on demand and fairly infrequently at that.

## How Did You Build It?
There are three main components of my URL shortener: The input endpoint that shortens URLs, the lookup endpoint that turns a short URL into the real deal, and the short code generator.

Let me start with that last one. I could have done something fancy to create my short codes like having an incrementing primary key that mapped to my three character sequences (e.g. `1=aaa, 2=aab, 3=aac, etc`) or some other mechanism to reliably generate these codes. Instead, I took the simple approach of randomly generating three characters within my 62 character range and assuming it would be fine. I then rely on the database to enforce uniqueness. I haven’t had any issues with this approach to date. Sure, in theory, I could get collisions and either fail or retry. Randomly generating codes until you get an unused one is not guaranteed to ever terminate but I’ve created probably a few hundred entries so far with no issues. It’s not like this being 100% reliable is the most critical thing in the world.

The lookup portion consists of a simple SQL query followed by a 302 redirect. That’s it!

Lastly, we have the input to create a short URL. I started with a simple web form that consisted only of an input box and submit button. This worked well: read the input, validate it, generate a short URL DB entry, and finally output the short code. Eventually, I supported a non-form interface for an integration with [Alfred](https://alfredapp.com) as well. With that, I have a working URL shortener! It’s deployable on Heroku as a small flask app that works fine with their free web and Postgres tiers for one person. I’ll note that this has been the first time I’ve used Postgres for any sort of app (I’ve always used MySQL for relational database storage before). There were a few differences but it has worked well for me thus far!

## How Do You Use This Shortener?
At first, I would load up the web form for my shortener, put the URL I wanted to shorten into the input box, and get back the short code. From there, I developed a shorthand to write the short URL into my paper notes: I use `s/{shortcode}` to denote a URL I might need. For example, I’d write  `s/xyz`  in my notes.This means that on paper I can denote any URL with five characters. That’s pretty great!

Once I developed this usage pattern and shorthand, I got to thinking about how I use the shortener. I decided that since I’m already a heavy Alfred user, I should try building a workflow for creating and consuming short URLs. I developed an API endpoint for shortening URLs that was safe from bots polluting my key namespace and a way to create/view short URLs.

Now that I have that done, my usage of the URL shortener is very simple: Open Alfred, type “s <URL>” to create a short URL. This will copy the short code to my clipboard and displays it in large text on my screen. Now, I can copy it down into whatever I was writing a note about in my shorthand (e.g. `s/xyz`). In order to look up that short code, I simply type `s/xyz` into Alfred and hit enter. It will open a browser to the fully qualified short URL and the shortener service will do the rest!

It isn’t a big project but it fits into this category of “personal infrastructure” applications that I've been thinking about and working on over time. Maybe I’ll write more about that topic in the future.

## Wishlist
The initial version of this service took a short time one afternoon. This was followed by the little bit of time to get the Alfred workflow going. After that, I’ve really not spent much (if any) time on this project. That said, I do have a small wish list that maybe I’ll get to one day:
- Be able to dump a mapping of all short codes to URLs
- Take this as an opportunity to learn how to build a Chrome extension
- Provide a way to manage (edit, delete) short codes (this is pretty low priority).
- Back up the Postgres DB regularly

## What I’ve learned and What I’m Thinking About
I’ll be honest: with my level of Python and web experience, this project wasn’t very complicated. It was enjoyable though! For one, I found a way to add simplicity and utility to my life with a minimal time investment. I also got to do a small amount of web development again during a time that I was doing totally different things at work. That was fun for me!

Lastly, it further supported this idea of personal infrastructure that I’ve had bouncing around my head for a while (and have also sort of discussed before with my friend [Alex](https://twitter.com/alexhaefner)). At a very high level, this concept is that very small custom apps can make my life easier/better in a number of ways. Since I’m a programmer, they are not a big investment to prototype out. I’ve thought about how this can improve the lives of non-technical people too but I have nothing super enlightening to report there at the moment.

Do you have any “personal infrastructure” projects? I’d love to hear about them!
