#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os
from pathlib import Path

HOME = str(Path.home())

THEME = os.path.join(HOME, 'dev/blue-penguin')

# Theme optional settings (theme set to blue-penguin)
ARCHIVES_URL = 'archives'
ARCHIVES_SAVE_AS = 'archives/index.html'
ARTICLE_URL = '{slug}'

MENU_INTERNAL_PAGES = (
    ('Archives', ARCHIVES_URL, ARCHIVES_SAVE_AS),
)

AUTHOR = 'David Wilemski'
SITENAME = "David's Blog"
SITEURL = ''

DEFAULT_METADATA = {
    'status': 'draft',
}

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = []

REL_ME_LINKS = "https://github.com/davidwilemski"

# Social widget
SOCIAL = (('Instagram', 'https://instagram.com/davidwilemski'),
          ('Strava', 'https://strava.com/athletes/dtw0'),
          ('Github', 'https://github.com/davidwilemski'),
          ('Twitter', 'https://twitter.com/davidwilemski'),)
SOCIAL = {
    'me': [
              ('Instagram', 'https://instagram.com/davidwilemski'),
              ('Strava', 'https://strava.com/athletes/dtw0'),
              ('Github', 'https://github.com/davidwilemski'),
              ('Twitter', 'https://twitter.com/davidwilemski'),
          ],
    'token_endpoint': "https://tokens.indieauth.com/token",
    'authorization_endpoint': "https://indieauth.com/auth",
    'authorization_endpoint': "https://indieauth.com/auth",
    'micropub': "https://davidwilemski.com/micropub"
}

DEFAULT_PAGINATION = 1

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
