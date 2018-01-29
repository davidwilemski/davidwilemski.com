Title: Productivity in a New Codebase
Date: 2018-01-28 23:50
Author: David Wilemski
Category: blog
Slug: productivity-new-codebase
Status: published

At the end of last year, I moved to a new team at work. 

I had spent a little over three years on my previous team where I worked on Facebook's container daemon, blob distribution mechanism, service orchestration system, and, mostly, tooling for developers that ties all these systems together so they are able to deploy services. 

A good portion of my time on the team was spent on debugging. Debugging production issues in our components. Debugging other people's services when they needed help. Debugging the interaction between the orchestration system and other people's services or deployment automation. Even debugging standard Linux utilities like `mount`. This meant that I got really comfortable diving into foreign code bases. I still believe this is maybe the best skill I developed in those three years.

That said, over the last few months I've learned the difference between spelunking through an unfamiliar codebase with a specific purpose and having a strong mental model of the codebase's structure, nuances, and quirks. Tracing an execution path backward to figure out why an error happens or figuring out what an undocumented flag does are sort of bottom-up exploration of a codebase. These seem pretty different from day to day work on modules and classes. At first, I was a little bit discouraged by this unproductive wall that I'd hit. I was still able to make contributions to my new codebase and had meetings with various new teammates where they explained various parts of the architecture. Even after all this, I felt that something was missing.

There's a difference between knowing how a system works at the architectural level and how it works at an implementation level. You might know that requests flow in and hit certain components in a specific order or understand the data model. That doesn't mean you _know_ what is happening when communicating with your data store or as requests flow through your web app. That level of understanding comes from reading and working with the code regularly.

Upon further reflection on my feeling I realized that over the last couple years the things I had prided myself on were (partially) derived from my deep knowledge of the code and systems I worked on every day. The ability to recognize flaws and proactively work towards resolution, to know what needed doing and prioritize across all of those options - these were skills that had become second nature, that I took deep satisfaction from. I then reminded myself that it hadn't always been that way. It took me between six months and a year to feel truly productive on my previous team. These abilities arose from long-term work on the codebase. Ramping up on a new project doesn't happen as if by magic just because you've successfully done so on a previous project. It takes work and, if I may theorize, it's a skill just like any other in that it probably gets easier with repetition. It's not a skill that we practice very often because we often stay working within a codebase for years at a time and ramping up is time-consuming.

So far, I've contributed where possible by identifying pain points that prevented me from more easily ramping up: Adding [Type Annotations](https://docs.python.org/3/library/typing.html) in more confusing portions of the codebase, refactored some of the more complex methods, and started addressing common oncall issues. While this is all helpful for developer productivity, it (mostly) doesn't impact the people using our product. I've also investigated a few reported bugs which have helped me gain a better end to end understanding of the system. I just have to continue to remind myself that productivity on a larger scale will come with time and effort.

What do you do to learn a new production codebase that is complex?
