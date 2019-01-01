#!/usr/bin/env python2
# --------------------------------------------------------------------
#
# Copyright (C) 2013 Marminator <cody_y@shaw.ca>
# Copyright (C) 2013 pao <patrick.oleary@gmail.com>
# Copyright (C) 2013 Daniel Triendl <daniel@pew.cc>
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# COPYING for more details.
#
# --------------------------------------------------------------------

import logging
import time
import requests
from bmscraper.ratelimiter import TokenBucket

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from bmscraper import BMScraper, UserscriptEmotesProcessorFactory

from data import *
from json import dumps
import os

CDN_ORIGIN = 'https://cdn.berrytube.tv/berrymotes'

factory = UserscriptEmotesProcessorFactory(single_emotes_filename=os.path.join('..', 'single_emotes', '{}', '{}.png'),
                                           apng_dir=os.path.join('..', 'images'),
                                           apng_url=CDN_ORIGIN + '/images/{}/{}')

scraper = BMScraper(factory)
scraper.user = os.environ['REDDIT_USERNAME']
scraper.password = os.environ['REDDIT_PASSWORD']
scraper.subreddits = subreddits
scraper.image_blacklist = image_blacklist
scraper.nsfw_subreddits = nsfw_subreddits
scraper.emote_info = emote_info
scraper.rate_limit_lock = TokenBucket(15, 30)
scraper.tags_data = requests.get(CDN_ORIGIN + "/data/tags.js").json()

start = time.time()
scraper.scrape()
logger.info("Finished scrape in {}.".format(time.time() - start))

f = open(os.path.join('..', 'data', 'berrymotes_data.js'), 'wb')
json = dumps(scraper.emotes, separators=(',', ':'))
f.write(''.join(["var berryEmotes=", json, ";"]))
f.close()

f = open(os.path.join('..', 'data', 'berrymotes_json_data.json'), 'wb')
f.write(dumps(scraper.emotes, separators=(',', ':')))
f.close()

for i, emote in enumerate(scraper.emotes):
    emote['id'] = i
    try:
        emote['tags'].remove('')
    except ValueError:
        pass
    emote['tags'].sort()

f = open(os.path.join('..', 'data', 'berrymotes_json_data.v2.json'), 'wb')
f.write(dumps(scraper.emotes, separators=(',', ':')))
f.close()
