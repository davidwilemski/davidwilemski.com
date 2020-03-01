Title: Parsing Photo Metadata - Part 1
Date: 2020-03-01 15:20
Author: David Wilemski
Category: blog
Tags: programming
Slug: photosort-part-1
Status: draft

_This is the initial post in what is intended to be a series where I write about what I learn while reverse engineering photo file formats with the goal of reading metadata (e.g. Exif). It isn't meant to be a definitive guide to the format but rather documenting the thought process of taking the format apart by only looking at file data rather than reading specifications, library implementations, or other more qualified information sources. Why? Because sometimes using `hexdump` and hacking together a custom tool is just more fun._

Towards the beginning of the year I was interested in writing a tool that would sort my photos into a directory tree that followed the `year/month/date/<file>` format. I have heard of such tools myself but wanted a little project I could work on for myself. To make it more fun, I wanted to see whether I could do this without any library support for reading Exif data out of photos and instead parse the needed information myself. It seemed to be the sort of thing that would be perfect for Rust (or any memory safe language, for that matter): reading a set of file data with unknown formats from usually trustworthy but sometimes potentially untrusted sources. I figured that I could start by implementing my sorting program but if I finished that and still had motivation to learn more about these formats that I could continue and write a generalized library. Whether I have that motivation is still TBD. I'll also note that I wanted to rely on the date embedded into the file rather than the file metadata provided by the filesystem (such as `ctime`) as that can be unreliable in certain circumstances.

Before I got started I did some basic searching and learned that the CR2 files that my Cannon cameras output in raw mode are only one of multiple "raw formats" and that they are not a standardized format. That's good to know, there's no spec to speak of anyhow! I did learn that there's a program called [`dcraw`](https://www.dechifro.org/dcraw/) which is a C program (not library!) maintained by Dave Coffin that supports most raw formats. This is more focused on processing the photos rather than extracting metadata. While I found that interesting, I didn't use it as a base for my program. I was open to researching further if I got stuck but so far have not needed to. With all that out of the way, let's dig in!

First off, I leaned pretty heavily on standard Unix tools for extracting the info that I wanted. `hexdump` and `strings` are your friends for this type of work. In this post I mostly focus on the output of `hexdump` but any hex editor would also do. The following is a `hexdump` of the first few hundred bytes of an image I took, the header does go on for a fair bit longer and I see things like the lens that I used and the aperture setting in that later output but for now I'm most concerned with extracting the date/time of the photo which is near the start of the file.

```
$ hexdump -C -n 320 photo.CR2
00000000  49 49 2a 00 10 00 00 00  43 52 02 00 4a b2 00 00  |II*.....CR..J...|
00000010  12 00 00 01 03 00 01 00  00 00 70 17 00 00 01 01  |..........p.....|
00000020  03 00 01 00 00 00 a0 0f  00 00 02 01 03 00 03 00  |................|
00000030  00 00 ee 00 00 00 03 01  03 00 01 00 00 00 06 00  |................|
00000040  00 00 0f 01 02 00 06 00  00 00 f4 00 00 00 10 01  |................|
00000050  02 00 0e 00 00 00 fa 00  00 00 11 01 04 00 01 00  |................|
00000060  00 00 7c 18 01 00 12 01  03 00 01 00 00 00 01 00  |..|.............|
00000070  00 00 17 01 04 00 01 00  00 00 34 61 1e 00 1a 01  |..........4a....|
00000080  05 00 01 00 00 00 1a 01  00 00 1b 01 05 00 01 00  |................|
00000090  00 00 22 01 00 00 28 01  03 00 01 00 00 00 02 00  |.."...(.........|
000000a0  00 00 32 01 02 00 14 00  00 00 2a 01 00 00 3b 01  |..2.......*...;.|
000000b0  02 00 01 00 00 00 00 00  00 00 bc 02 01 00 00 20  |............... |
000000c0  00 00 c4 b2 00 00 98 82  02 00 01 00 00 00 00 00  |................|
000000d0  00 00 69 87 04 00 01 00  00 00 be 01 00 00 25 88  |..i...........%.|
000000e0  04 00 01 00 00 00 72 aa  00 00 74 b1 00 00 08 00  |......r...t.....|
000000f0  08 00 08 00 43 61 6e 6f  6e 00 43 61 6e 6f 6e 20  |....Canon.Canon |
00000100  45 4f 53 20 37 37 44 00  00 00 00 00 00 00 00 00  |EOS 77D.........|
00000110  00 00 00 00 00 00 00 00  00 00 48 00 00 00 01 00  |..........H.....|
00000120  00 00 48 00 00 00 01 00  00 00 32 30 32 30 3a 30  |..H.......2020:0|
00000130  32 3a 30 31 20 31 34 3a  33 32 3a 31 34 00 00 00  |2:01 14:32:14...|
00000140  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
```

Let's note down some relevant metadata that we can see here. I don't particularly need this right now for _sorting_ but noting it for later: 245 bytes in we can see the the brand, a null byte, and the model name of my camera. `Canon` and `Canon EOS 77D`. It sort of seems like the manufacturer of the camera (Cannon) is delimited by a null after which the model is included. There are quite a few null bytes following this so it's the model is a fixed-width string where the nulls are used to pad out to particular offsets or there's some delimiter patten that I haven't recognized yet.

Now for the stuff I need to do directory sorting: We can see that 298 bytes in we have the a bunch of null bytes (and a random 'H'...) and the start of our date string: `2020:0`. The next line of our hexdump output gives us the second half of the date, a space, and the time: `2:01 14:32:14`. Three null bytes trail that. Putting that all together we get our date/time of `2020:02:01 14:32:14`!

Now, I'm guessing that the metadata fields are not aligned around 16 byte lines like our hexdump output is here. It isn't immediately clear what, if any, line oriented alignment there might be on this data. There certainly appear to be a lot of null bytes surrounding the useful data. Perhaps it's just a lot of data packed in at various offsets and my particular camera doesn't populate most of the fields. 🤷

For a very brittle first implementation of date all I had to do was hard code this offset into my sorting program, read the next 10 bytes and parse that to get my directory structures. You can see the [parsing logic](https://github.com/davidwilemski/photosort/blob/3b8950f38c3326cfdd86ee0dcc19a284b9f009f1/src/main.rs) in the first commit of my photo sorting tool. That commit only parsed and printed dates, didn't quite sort all of the photos just yet. The [second commit](https://github.com/davidwilemski/photosort/commit/275cf6905b903de80e7dac287157a218c3b1c3db) took the set of bytes that represented the date and wired up logic to do file renaming. If you read through that, you'll note there was also a mode to rename using `git` rather than straight filesystem renames. That is because some of my photos are managed by [`git-annex`](https://git-annex.branchable.com/) and provides some extra safety on these operations so that anything can be undone so that I don't lose any data.

It turned out that this very unreliable implementation works! But only for photos taken with this particular camera in this particular format. Some older CR2 files I have from a different Cannon camera have a really similar structure but different offset for the date. Additionally, JPG file written by both of these cameras have JPG magic number stuff prefixing all this metadata so we'll have to build something more reliable. We'll start covering all this in more detail in part 2.
